((window, $) ->

  ($ '#handle-list').filtered
    selector: 'a'
    input: '#handle-filter'
    getText: (element) ->
      $.trim(($ element).text()).toLowerCase()

) this, this.jQuery
