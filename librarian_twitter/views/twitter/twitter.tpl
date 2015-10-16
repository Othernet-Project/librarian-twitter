<%inherit file='/base.tpl'/>
<%namespace name='tweet_list' file='_tweet_list.tpl'/>
<%namespace name='handle_selector' file='_handle_selector.tpl'/>

<%namespace name="ui" file="/ui/widgets.tpl"/>

<%block name="title">
## Translators, used as page title
${_('Twitter')}
</%block>

##<%block name="extra_head">
##    <link rel="stylesheet" href="${assets['css/twitter']}">
##</%block>


${handles}

##<%block name="extra_scripts">
    ##<script src="${assets['js/twitter']}"></script>
##</%block>
