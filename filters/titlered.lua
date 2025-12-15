function Div(el)
  -- Check if this is a titlered div
  if el.classes:includes('titlered') then
    -- Check if we're producing LaTeX output
    if FORMAT:match 'latex' then
      -- Extract the header content
      local header_level = nil
      local header_content = {}
      
      -- Find the header element in the div
      for i, block in ipairs(el.content) do
        if block.t == 'Header' then
          header_level = block.level
          header_content = block.content
          break
        end
      end
      
      -- If we found a header, process it
      if header_level then
        -- Convert header content to inline string
        local content_str = pandoc.utils.stringify(header_content)
        
        -- Determine font size based on header level
        local font_sizes = {'\\LARGE', '\\Large', '\\large', '\\normalsize', '\\normalsize', '\\normalsize'}
        local font_size = font_sizes[header_level] or '\\normalsize'
        
        -- Create the LaTeX code with tight colorbox
        local latex_code = string.format(
          '\\noindent{\\setlength{\\fboxsep}{3pt}\\colorbox[HTML]{B32121}{\\makebox[\\dimexpr\\linewidth-2\\fboxsep][l]{\\color{white}%s\\bfseries\\hspace{0.5em}\\CrossMaltese\\hspace{-0.75em}%s}}}',
          font_size,
          content_str
        )
        
        -- Return as raw LaTeX block
        return pandoc.RawBlock('latex', latex_code)
      end
    end
  end
  
  -- Return unchanged if not titlered or not LaTeX
  return el
end