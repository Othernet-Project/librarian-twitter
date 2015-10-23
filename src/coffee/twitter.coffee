((window, $) ->

  ($ '#handle-list').filtered
    selector: 'a'
    input: '#handle-filter'
    getText: (element) ->
      element = $ element
      text = element.text().trim()
      text.toLowerCase()

) this, this.jQuery
