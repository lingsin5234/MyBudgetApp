# Budget App
This project is created to replace a spreadsheet that I use to track my finances.
I tend to spend a lot of time inputting data into the spreadsheet and then balancing
the columns afterwards, thus I thought of creating this app to not only help with the
balancing, but also display the data in a more visual manner.

My GitLab repo is: [Budget App](https://gitlab.com/lingsin5234/MyBudgetApp)

## Layout
The Models and Forms in Django are for me to input my daily expenses, earnings, etc.
The Views help facilitate the templates based on which link I use, for example:

    /upload/expenses

This would indicate to use the upload page and the expense form to input data to the
Expense Line Items model.

## Data
Most data is made up as I went along with the testing. I use this app on my local machine,
so there is no real data stored on the server that hosts my Django applications.

## D3.js
I once again explore D3.js in this app, in hopes of providing better visuals for myself to
filter, sort and group my budgeting data. I hope to explore different types of graphs
in the near future based on types of line items and categories.
