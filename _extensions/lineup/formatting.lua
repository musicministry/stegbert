-- formatting.lua
-- Lua filter for Pandoc/Quarto: PDF rendering of upcoming.qmd.
--
-- IMPORTANT: This filter uses a top-level Pandoc(doc) function to read
-- metadata (pdf-colwidths) before processing tables. Defining both
-- Meta() and Table() at the top level causes Meta() to never fire in
-- some Pandoc versions, so all logic is unified here.

-- ============================================================
-- Helpers
-- ============================================================
local function blocks_to_latex(blocks)
  return pandoc.write(pandoc.Pandoc(blocks), "latex"):gsub("%s+$", "")
end

local function blocks_to_html(blocks)
  return pandoc.write(pandoc.Pandoc(blocks), "html"):gsub("%s+$", "")
end

local function inlines_to_latex(inlines)
  return blocks_to_latex({pandoc.Plain(inlines)})
end

local function is_pdf()
  return FORMAT:match("latex") or FORMAT:match("pdf")
end

-- ============================================================
-- Read pdf-colwidths from document metadata.
-- Returns a list of numbers, or nil if not set.
-- ============================================================
local function read_colwidths(meta)
  if not meta["pdf-colwidths"] then return nil end
  local widths = {}
  for _, v in ipairs(meta["pdf-colwidths"]) do
    local n = tonumber(pandoc.utils.stringify(v))
    if n then table.insert(widths, n) end
  end
  return #widths > 0 and widths or nil
end

-- ============================================================
-- Transform a single Div element
-- ============================================================
local function transform_div(el)
  if is_pdf() then
    if el.attributes["when-format"] == "html" then return {} end
    for _, cls in ipairs(el.classes) do
      if cls == "titlered" then return {} end
    end
  end

  for _, cls in ipairs(el.classes) do
    if cls == "schedule-callout" then
      local title = el.attributes["title"] or "Note"
      if is_pdf() then
        local body = blocks_to_latex(el.content)
        return {pandoc.RawBlock("latex", string.format(
          "\\vspace{1em}\n\\begin{calloutimportant}[%s]\n%s\n\\end{calloutimportant}\n\\vspace{1em}",
          title, body))}
      else
        -- Return a native Pandoc Div with Quarto's callout classes so
        -- Quarto processes it normally for HTML (styling, icon, title).
        -- The title is set via the custom-title attribute, which Quarto
        -- reads when rendering callout-important divs.
        local callout_div = pandoc.Div(
          el.content,
          pandoc.Attr("", {"callout-important"}, {["title"] = title})
        )
        return {callout_div}
      end
    end
  end
end

-- ============================================================
-- Transform a Span with class .red -> \textcolor{schedred}{...}
-- Use in .qmd as [some text]{.red} for red text in both HTML and PDF.
-- HTML color is handled via CSS; this handles the PDF side.
-- ============================================================
local function transform_colored_span(el)
  if not is_pdf() then return end
  for _, cls in ipairs(el.classes) do
    if cls == "red" then
      local text = inlines_to_latex(el.content)
      return pandoc.RawInline("latex",
        string.format("\\textcolor{schedred}{%s}", text))
    end
  end
end

-- ============================================================
-- Transform a single Span element
-- Two float:right spans appear per week:
--   1. [Feast Name]{style="float:right"}  inside the #### heading
--      → \hfill\cross{}\enspace{} Feast Name  (cross between date and name)
--   2. [**Mass Setting:** [...]]{style="float:right"} standalone para
--      → \hfill\textbf{Mass Setting:} ...       (no cross, plain right-align)
-- Distinguish by checking if the first real inline child is Strong (bold).
-- The Mass Setting span always starts with **Mass Setting:**; feast names don't.
-- ============================================================
local function transform_span(el)
  if not is_pdf() then return end
  local style = el.attributes["style"] or ""
  if not style:match("float%s*:%s*right") then return end

  -- Check whether this span starts with a Strong (bold) node
  local is_mass_setting = false
  for _, inline in ipairs(el.content) do
    if inline.t == "Space" or inline.t == "SoftBreak" then
      -- skip leading whitespace
    elseif inline.t == "Strong" then
      is_mass_setting = true
      break
    else
      break
    end
  end

  local prefix
  if is_mass_setting then
    -- Mass Setting line: push everything to the right
    prefix = pandoc.RawInline("latex", "\\hfill{}")
  else
    -- Feast name in heading: just cross + thin space, NO \hfill.
    -- The date and feast name stay together on the left.
    -- (The \hfill on the mass setting line below handles right-alignment.)
    prefix = pandoc.RawInline("latex", "\\cross{}\\enspace{}")
  end

  local result = {prefix}
  for _, inline in ipairs(el.content) do
    table.insert(result, inline)
  end
  return result
end

-- ============================================================
-- Transform a Link: internal #anchors -> \hyperref
-- ============================================================
local function transform_link(el)
  if not is_pdf() then return end
  local target = el.target or ""
  if target:match("^#") then
    local anchor = target:sub(2)
    local text = inlines_to_latex(el.content)
    return pandoc.RawInline("latex",
      string.format("\\hyperref[%s]{%s}", anchor, text))
  end
end

-- ============================================================
-- Transform a RawInline: HTML entities
-- ============================================================
local function transform_rawinline(el)
  if not is_pdf() then return end
  if el.format == "html" then
    local s = el.text
    s = s:gsub("&nbsp;",   "~")
    s = s:gsub("&#x2720;", "\\cross{}")
    s = s:gsub("&#9760;",  "\\cross{}")
    if s ~= el.text then return pandoc.RawInline("latex", s) end
    return {}
  end
end

-- ============================================================
-- Transform a RawBlock: drop HTML blocks in PDF
-- ============================================================
local function transform_rawblock(el)
  if not is_pdf() then return end
  if el.format == "html" then return {} end
end

-- ============================================================
-- Transform a BulletList: replace default bullets with \cross{}.
-- The simplest approach: let Pandoc emit the itemize environment
-- normally, then do a string replacement of \item with \item[\cross{}].
-- ============================================================
local function transform_bulletlist(el)
  if not is_pdf() then return end
  -- Render the whole list normally via Pandoc
  local latex = blocks_to_latex({pandoc.BulletList(el.content)})
  -- Replace every \item with \item[\cross{}]
  latex = latex:gsub("\\item", "\\item[\\cross{}]")
  return {pandoc.RawBlock("latex", latex)}
end

-- ============================================================
-- Transform a Table: minipage + tabular, no rules, cross in col 1,
-- raggedright on cols 2+, optional pdf-colwidths override.
-- ============================================================
local function transform_table(el, colwidths_override)
  if not is_pdf() then return end

  local ncols = #el.colspecs
  local widths = {}
  if colwidths_override and #colwidths_override == ncols then
    widths = colwidths_override
  else
    for _, cs in ipairs(el.colspecs) do
      table.insert(widths, cs[2] or 0)
    end
  end

  local nseps = (ncols - 1) * 2
  local col_parts = {}
  for i, w in ipairs(widths) do
    if w and w > 0 then
      local dim = string.format(
        "\\dimexpr %.4f\\linewidth - %d\\tabcolsep\\relax", w, nseps)
      if i == 1 then
        table.insert(col_parts, "p{" .. dim .. "}")
      else
        table.insert(col_parts,
          ">{\\raggedright\\arraybackslash}p{" .. dim .. "}")
      end
    else
      table.insert(col_parts, "l")
    end
  end
  local col_str = "@{}" .. table.concat(col_parts, " ") .. "@{}"

  local all_rows = {}
  if el.head and el.head.rows then
    for _, r in ipairs(el.head.rows) do table.insert(all_rows, r) end
  end
  for _, body in ipairs(el.bodies) do
    for _, r in ipairs(body.body) do table.insert(all_rows, r) end
  end

  local em_space = "\xe2\x80\x83"
  local row_strings = {}
  for _, row in ipairs(all_rows) do
    local cells = {}
    for col_i, cell in ipairs(row.cells) do
      local content = blocks_to_latex(cell.contents)
      content = content:gsub("^%s+", ""):gsub("%s+$", "")
      table.insert(cells, content)
    end
    -- Emit extra vertical space after natural liturgical section breaks.
    -- Add or remove entries from extra_space_after to taste.
    local col1 = cells[1] or ""
    local extra_space_after = {
      "Processional", "Gloria", "Gospel Acclamation", "Lamb of God", "Offertory",
      "Communion", "Meditation", "Veneration of the Cross", "Litany of the Saints", "Washing of Feet"
    }
    local row_sep = " \\\\[2pt]"
    for _, part in ipairs(extra_space_after) do
      if col1:find(part, 1, true) then
        row_sep = " \\\\[1.25em]"
        break
      end
    end
    table.insert(row_strings, table.concat(cells, " & ") .. row_sep)
  end

  return {pandoc.RawBlock("latex", string.format(
    "\\begin{minipage}{\\linewidth}\n" ..
    "\\renewcommand{\\arraystretch}{1.2}\n" ..
    "\\begin{tabular}{%s}\n" ..
    "%s\n" ..
    "\\end{tabular}\n" ..
    "\\end{minipage}\\vspace{1em}",
    col_str, table.concat(row_strings, "\n")))}
end

-- ============================================================
-- Main entry point: Pandoc(doc) reads metadata first, then
-- walks the document applying all transformations.
-- ============================================================
function Pandoc(doc)
  local colwidths = read_colwidths(doc.meta)

  -- Walk the document, applying all transforms
  doc = doc:walk({
    BulletList = transform_bulletlist,
    Div       = transform_div,
    Span      = function(el)
      return transform_colored_span(el) or transform_span(el)
    end,
    Link      = transform_link,
    RawInline = transform_rawinline,
    RawBlock  = transform_rawblock,
    Table     = function(el) return transform_table(el, colwidths) end,
  })

  return doc
end