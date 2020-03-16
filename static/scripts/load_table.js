// declarations
var choices = ["Expense", "Revenue"];
var line_items = expense;

// drop-down boxes - not inside SVG.
var dd_box = d3.select('#select-data').append('select')
    .attr('class', 'select')
    .attr('id', 'dd_box')
    .on('change', onChange);

var dd_options = dd_box.selectAll('option')
    .data(choices).enter()
    .append('option')
        .text(function (d) { return d; });

function onChange() {
    selectValue = d3.select('#dd_box').property('value')
    if (selectValue == "Expense") {
        line_items = expense
        load_table();
    }
    else {
        line_items = revenue;
        load_table();
    }
};

// load table data
function load_table() {

    // remove all previous tables
    d3.select('#show-data').selectAll('table').remove();

    // table set up
    var table = d3.select('#show-data').append('table')
        .attr('style', 'margin-left: 250px');
    var thead = table.append('thead');
    var tbody = table.append('tbody');

    // header
    var header = thead.append('tr');
    var header_values = ["name", "category", "amount", "date_stamp"];
    var col_names = header.selectAll('th')
        .data(header_values).enter().append('th')
        .text(function(d) { return d; });

    var rows = tbody.selectAll('tr')
        .data(line_items).enter().append('tr');

    var cells = rows.selectAll('td')
        .data(function(row) {
            return header_values.map(function(col) {
                return {column: col, value: row[col]};
            });
        }).enter().append('td')
        .text(function(d) { return d.value; });
}

// load table once on page load
load_table();
