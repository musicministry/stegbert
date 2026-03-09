-- Source - https://stackoverflow.com/a
-- Posted by TomBen
-- Retrieved 2025-12-27, License - CC BY-SA 4.0

function Link(link)
  if link.target:match '^https?%:' then
    link.attributes.target = '_blank'
    return link
  end
end
