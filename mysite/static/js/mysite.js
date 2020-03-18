<script src="//code.jquery.com/jquery-1.11.2.min.js"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/8.5/highlight.min.js"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/lightbox2/2.7.1/js/lightbox.min.js"></script>

<script type="text/javascript">
    $(document).ready(function () {
      // Default syntax highlighting
      hljs.initHighlightingOnLoad();

      // Header
      var menuToggle = $('#js-mobile-menu').unbind();
      $('#js-navigation-menu').removeClass("show");
      menuToggle.on('click', function (e) {
        e.preventDefault();
        $('#js-navigation-menu').slideToggle(function () {
          if ($('#js-navigation-menu').is(':hidden')) {
            $('#js-navigation-menu').removeAttr('style');
          }
        });
      });
    });

</script>