-- function Header(el)
--   -- Check if we're producing LaTeX output
--   if FORMAT:match 'latex' then
--     -- Look for spans with float:right style
--     local main_content = {}
--     local float_right_content = {}
    
--     for i, inline in ipairs(el.content) do
--       if inline.t == 'Span' and inline.attributes.style then
--         -- Check if the style contains float:right
--         if string.match(inline.attributes.style, 'float%s*:%s*right') then
--           -- Extract color if present
--           color = 'B32121'
          
--           -- Start building the right-side content
--           if color then
--             -- Add color command
--             table.insert(float_right_content, pandoc.RawInline('latex', '\\textcolor[HTML]{' .. color .. '}{'))
--           end
          
--           -- Add this content to float_right_content
--           for _, item in ipairs(inline.content) do
--             table.insert(float_right_content, item)
--           end
          
--           -- Close color command if we opened it
--           if color then
--             table.insert(float_right_content, pandoc.RawInline('latex', '}'))
--           end
--         else
--           table.insert(main_content, pandoc.RawInline('latex', '\\textcolor[HTML]{' .. color .. '}{'))
--           table.insert(main_content, inline)
--           table.insert(float_right_content, pandoc.RawInline('latex', '}'))
--         end
--       else
--         table.insert(main_content, inline)
--       end
--     end
    
--     -- If we found float:right content, create LaTeX with hfill
--     if #float_right_content > 0 then
--       -- Build new content: main text + \hfill + right-aligned text
--       local new_content = {}
      
--       -- Add main content
--       for _, item in ipairs(main_content) do
--         table.insert(new_content, pandoc.RawInline('latex', '\\textcolor[HTML]{' .. color .. '}{'))
--         table.insert(new_content, item)
--         table.insert(float_right_content, pandoc.RawInline('latex', '}'))
--       end
      
--       -- Add \hfill to push the rest to the right
--       table.insert(new_content, pandoc.RawInline('latex', '\\hfill '))
      
--       -- Add float:right content
--       for _, item in ipairs(float_right_content) do
--         table.insert(new_content, item)
--       end
      
--       -- Update the header content
--       el.content = new_content
--     end
--   end
  
--   return el
-- end

-- Process inline spans with float:right
function process_inlines(inlines, is_header)
  if not FORMAT:match 'latex' then
    return inlines
  end
  
  local main_content = {}
  local float_right_items = {}
  local has_float_right = false
  local float_right_color = nil
  
  for i, inline in ipairs(inlines) do
    if inline.t == 'Span' and inline.attributes.style then
      -- Check if the style contains float:right
      if string.match(inline.attributes.style, 'float%s*:%s*right') then
        has_float_right = true
        
        -- Extract color if present in inline style
        float_right_color = string.match(inline.attributes.style, 'color%s*:%s*#?([%w]+)')
        
        -- If no inline color and this is a header, use the CSS color
        if not float_right_color and is_header then
          float_right_color = 'B32121'  -- Your CSS color from .titlered
        end
        
        -- Store the inline content items
        for _, item in ipairs(inline.content) do
          table.insert(float_right_items, item)
        end
      else
        table.insert(main_content, inline)
      end
    else
      table.insert(main_content, inline)
    end
  end
  
  -- If we found float:right content, create LaTeX with proper positioning
  if has_float_right then
    local new_content = {}
    
    -- For headers, wrap main content in color
    if is_header then
      table.insert(new_content, pandoc.RawInline('latex', '\\textcolor[HTML]{B32121}{'))
    end
    
    -- Add main content
    for _, item in ipairs(main_content) do
      table.insert(new_content, item)
    end
    
    -- Close color for main content if header
    if is_header then
      table.insert(new_content, pandoc.RawInline('latex', '}'))
    end
    
    -- Use leaders to fill space, then add the right-aligned text
    table.insert(new_content, pandoc.RawInline('latex', '\\hspace*{\\fill}\\mbox{'))
    
    if float_right_color then
      table.insert(new_content, pandoc.RawInline('latex', '\\textcolor[HTML]{' .. float_right_color .. '}{'))
    end
    
    -- Add float:right content
    for _, item in ipairs(float_right_items) do
      table.insert(new_content, item)
    end
    
    if float_right_color then
      table.insert(new_content, pandoc.RawInline('latex', '}'))
    end
    
    table.insert(new_content, pandoc.RawInline('latex', '}'))
    
    return new_content
  end
  
  return inlines
end

-- Handle headers
function Header(el)
  el.content = process_inlines(el.content, true)  -- Pass true to indicate this is a header
  return el
end

-- Handle paragraphs
function Para(el)
  el.content = process_inlines(el.content, false)
  return el
end

-- Handle plain text blocks
function Plain(el)
  el.content = process_inlines(el.content, false)
  return el
end