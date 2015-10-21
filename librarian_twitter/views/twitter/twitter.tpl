<%inherit file="/narrow_base.tpl"/>
<%namespace name='tweet_list' file='_tweet_list.tpl'/>
<%namespace name='handle_selector' file='_handle_selector.tpl'/>

<%namespace name="ui" file="/ui/widgets.tpl"/>

<%block name="title">
## Translators, used as page title
${_('Twitter')}
</%block>

<%block name="extra_head">
    <link rel="stylesheet" href="${assets['css/twitter']}">
</%block>

<%block name="menubar_panel">
    <input id="twitter-filter" placeholder="Twitter filter">
</%block>

<%block name="narrow_main">
    <div id="tabbable-twitter" class="o-tabbable">
        <ul class="o-tab-handles" role="tablist">
            <li class="o-tab-handle">
            ${ui.tab_activator(_('Tweets'), 'tweets', 'tweet-tab', active=True)}
            </li>
            <li class="o-tab-handle">
            ${ui.tab_activator(_('Handles'), 'handles', 'handle-tab')}
            </li>
        </ul>

        <div class="o-tab-panels">
            <%ui:tab_panel id="tweet-tab" expanded="true">
                % for tweet in tweets:
                    <div class="tweet" id="${tweet['id']}>
                        <img class="twitter-icon" src="icon.png">
                        <p class="tweet-header">
                            <span class="handle">
                                ${tweet['handle']}
                            </span>
                            <span class="tweet-img">
                                ${tweet['img']}
                            </span>
                            <span class="tweet-timestamp">
                                ${tweet['timestamp']}
                            </span>
                        </p>
                        <span class="tweet-text">
                            ${tweet['tweet']}
                        </span>
                    </div>
                % endfor
            </%ui:tab_panel>

            <%ui:tab_panel id="handle-tab">
                % for handle in handles:
                    <a href="${i18n_url('twitter', h=handle[0])}">
                        ${handle[0]}
                    </a>
                % endfor
            </%ui:tab_panel>
        </div>
    </div>
</%block>

<%block name="extra_scripts">
    <script src="${assets['js/twitter']}"></script>
</%block>
