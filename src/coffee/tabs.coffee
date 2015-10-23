((window, $) ->

  win = $ window
  baseUrl = window.twitterBaseUrl
  QS_RE = /section=([^&]+)/


  onTabChange = (e, tab, panel) ->
    section = (panel.attr 'id').replace '-tab', ''
    url = baseUrl + section
    window.history.pushState null, null, url
    return


  getSection = () ->
    # Obtain section from query params
    q = window.location.search
    match = QS_RE.exec(q) || []
    match[1]


  twitterTabs = $ '#tabbable-twitter'
  twitterTabs.tabable()
  twitterTabs.on 'tabchange', onTabChange


  win.on 'popstate', (e) ->
    section = getSection()
    if not section
      return
    twitterTabs.tabbableCloseAll()
    twitterTabs.tabbableOpenTab "#{section}-tab", true
    return

  return

) this, this.jQuery
