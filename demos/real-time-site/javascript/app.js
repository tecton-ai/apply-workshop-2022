var $ = require('jquery');

const getOnlineRecs = async (userId, movieId) => {
  const url =  'http://localhost:5001/recommend-next/' + userId + '/' + movieId + '/';
  const response = await fetch(url);
  const recJson = await response.json(); //extract JSON from the http response
  return recJson['recommended_titles']
}


const getBatchRecs = async (userId) => {
  const url =  'http://localhost:5000/recommendations/' + userId + '/';
  const response = await fetch(url);
  const recJson = await response.json(); //extract JSON from the http response
  return recJson['recommended_titles']
}

function renderTable(recs) {
    var table = document.createElement('recomendationTable');
    for (var i = 0; i < recs.length; i++) {
        var row = document.createElement('tr');
        var cell = document.createElement('td');
        cell.textContent = recs[i];
        row.appendChild(cell);
        table.appendChild(row);
    }
    var div = $('#recommendationsContainer');
    div.empty().append(table);
}

$(document).ready(function() {
  var button = $('#getRecommendationsButton');
  var userSelector = $('#userSelector');
  var movieSelector = $('#movieSelector');
  userSelector.change(function () {
      if ('' == userSelector.val()) {
          button.attr('disabled', 'disabled');
      } else {
          button.removeAttr('disabled');
      }
  });

  button.click(async function(event) {
      recs = await getOnlineRecs(userSelector.val(), movieSelector.val());
      renderTable(recs)
      console.log(recs)
      event.preventDefault();
  });
});
