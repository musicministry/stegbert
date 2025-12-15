-- Function to escape special LaTeX characters
function escape_latex(text)
  text = string.gsub(text, '&', '\\&')
  text = string.gsub(text, '%%', '\\%%')
  text = string.gsub(text, '%$', '\\$')
  text = string.gsub(text, '#', '\\#')
  text = string.gsub(text, '_', '\\_')
  text = string.gsub(text, '{', '\\{')
  text = string.gsub(text, '}', '\\}')
  text = string.gsub(text, '~', '\\textasciitilde{}')
  text = string.gsub(text, '%^', '\\textasciicircum{}')
  return text
end

-- Function to process cell contents including hyperlinks and formatting
function process_cell_inlines(inlines)
  local result = {}
  for _, inline in ipairs(inlines) do
    if inline.t == 'Link' then
      -- Handle hyperlinks
      local link_text = process_cell_inlines(inline.content)
      local url = inline.target
      table.insert(result, '\\href{' .. url .. '}{' .. link_text .. '}')
    elseif inline.t == 'Strong' then
      -- Handle bold text
      local bold_text = process_cell_inlines(inline.content)
      table.insert(result, '\\textbf{' .. bold_text .. '}')
    elseif inline.t == 'Emph' then
      -- Handle italic text
      local italic_text = process_cell_inlines(inline.content)
      table.insert(result, '\\textit{' .. italic_text .. '}')
    elseif inline.t == 'Code' then
      -- Handle inline code
      table.insert(result, '\\texttt{' .. escape_latex(inline.text) .. '}')
    elseif inline.t == 'Strikeout' then
      -- Handle strikethrough
      local strike_text = process_cell_inlines(inline.content)
      table.insert(result, '\\sout{' .. strike_text .. '}')
    elseif inline.t == 'Superscript' then
      -- Handle superscript
      local super_text = process_cell_inlines(inline.content)
      table.insert(result, '\\textsuperscript{' .. super_text .. '}')
    elseif inline.t == 'Subscript' then
      -- Handle subscript
      local sub_text = process_cell_inlines(inline.content)
      table.insert(result, '\\textsubscript{' .. sub_text .. '}')
    elseif inline.t == 'Str' then
      table.insert(result, escape_latex(inline.text))
    elseif inline.t == 'Space' then
      table.insert(result, ' ')
    elseif inline.t == 'SoftBreak' or inline.t == 'LineBreak' then
      table.insert(result, ' ')
    else
      -- For other inline types, stringify and escape
      table.insert(result, escape_latex(pandoc.utils.stringify({inline})))
    end
  end
  return table.concat(result)
end

function Table(el)
  -- Check if we're producing LaTeX output
  if FORMAT:match 'latex' then
    -- Start building the LaTeX table
    local latex_lines = {}
    
    -- Start minipage to prevent page breaks
    table.insert(latex_lines, '\\begin{minipage}{\\textwidth}')
    
    -- Determine number of columns
    local num_cols = #el.colspecs
    
    -- Create column specification that spans full width
    -- Use p{width} for columns that will stretch to fill
    local col_spec = 'p{0.02\\textwidth}p{0.25\\textwidth}p{0.73\\textwidth}'
    
    -- Start tabular with full text width and extra row spacing
    table.insert(latex_lines, '{\\renewcommand{\\arraystretch}{1.5}')
    table.insert(latex_lines, '\\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill}}' .. col_spec .. '}')
    table.insert(latex_lines, '\\arrayrulecolor{gray}\\hline')
    table.insert(latex_lines, '\\arrayrulecolor{black}')  -- Reset to black for any other lines
    table.insert(latex_lines, '\\noalign{\\vskip 0.5em}')  -- Add space after top line
    
    -- Process header if it exists
    if el.head and el.head.rows and #el.head.rows > 0 then
      for _, row in ipairs(el.head.rows) do
        local cells = {}
        for _, cell in ipairs(row.cells) do
          local cell_content = process_cell_inlines(cell.contents[1].content)
          table.insert(cells, cell_content)
        end
        table.insert(latex_lines, table.concat(cells, ' & ') .. ' \\\\')
      end
    end
    
    -- Process body rows
    for _, body in ipairs(el.bodies) do
      for i, row in ipairs(body.body) do
        local cells = {}
        for _, cell in ipairs(row.cells) do
          local cell_content = process_cell_inlines(cell.contents[1].content)
          table.insert(cells, cell_content)
        end
        -- Add row without bottom line
        table.insert(latex_lines, table.concat(cells, ' & ') .. ' \\\\')
      end
    end
    
    -- End tabular and minipage (no bottom line)
    table.insert(latex_lines, '\\end{tabular*}}')  -- Close the arraystretch group
    table.insert(latex_lines, '\\end{minipage}')
    table.insert(latex_lines, '')  -- Add blank line for spacing
    
    -- Return as raw LaTeX block
    return pandoc.RawBlock('latex', table.concat(latex_lines, '\n'))
  end
  
  -- Return unchanged if not LaTeX
  return el
end