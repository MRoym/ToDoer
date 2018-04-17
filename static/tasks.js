

var itemhtml = "";

$(document).ready(function(){


  $('#modal-form').click(function(event) {

    $("#form").modal({
    fadeDuration: 1000,
    fadeDelay: 0.50

    });
    $('input').attr('autocomplete','off');

  });

  var groups = []

  $.ajax({url: "/groups",
          success: function(result){

              groups = result;
              $('#at-input').atwho({
              at: "#",
              headerTpl: "<b>Your groups</b>",
              insertTpl: "${atwho-at}${name}",
              data: groups,
              limit: 5,

            });

      }
    });

  var tabs = document.getElementsByClassName("tab");
  tabs[0].className += " active";
  var cont = document.getElementsByClassName("tab-content");
  cont[0].className += " active-content";

});


function openTab(evt, group) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].className = tabcontent[i].className.replace(/ active-content/g, "");
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tab");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(group).className += " active-content"
    evt.currentTarget.parentNode.className += " active";
}
