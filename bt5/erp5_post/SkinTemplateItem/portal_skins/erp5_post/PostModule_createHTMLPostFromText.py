return context.PostModule_createHTMLPost(
  follow_up=follow_up,
  predecessor=predecessor,
  data="<p>" + data.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("  ", " &nbsp;").replace("\n", "<br/>") + "</p>",
)
