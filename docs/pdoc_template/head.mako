<%!
    from pdoc.html_helpers import minify_css
%>
<%def name="homepage()" filter="minify_css">
    .homepage {
        display: block;
        font-size: 2em;
        font-weight: bold;
        color: #555;
        padding-bottom: .5em;
        border-bottom: 1px solid silver;
    }
    .homepage:hover {
        color: inherit;
    }
    .homepage img {
        max-width:20%;
        max-height: 5em;
        margin: auto;
        margin-bottom: .3em;
    }
</%def>

<style>${homepage()}</style>
<link rel="icon" href="https://www.aegisblade.com/images/BigCloud.png">
