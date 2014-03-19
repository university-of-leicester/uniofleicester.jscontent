$(document).ready(function() {
  $('.uol-tabs').easytabs({
      tabs: ".uol-tabs-head > ul > li",
      tabActiveClass: "tab-selected"
  });
    var allPanels = $('.uol-accordion-body').hide();

  $('.show-all').click(function(evt) {
    evt.preventDefault();
    var allSections = $(this).parents(".uol-accordion").find(".uol-accordion-section");
    var allPanels = allSections.find('.uol-accordion-body');
    var some_hidden = allPanels.filter(':hidden').length > 0;

    if (some_hidden) {
        allPanels.show();
    } else {
        allPanels.hide();
    };
  });

  $('.uol-accordion-head > a').click(function(evt) {
    evt.preventDefault();
    var $body = $(this).parent().next()
    $body.slideToggle();
  });

});



