// script.js 
// Get form, expense list, and total amount elements 

const expenseForm = 
	document.getElementById("expense-form"); 
const expenseList = 
	document.getElementById("expense-list"); 
const totalAmountElement = 
	document.getElementById("total-amount"); 

// Get the current date
const currentDate = new Date();

// Format the date as yyyy-MM-dd
const formattedDate = `${currentDate.getFullYear()}-${(currentDate.getMonth() + 1).toString().padStart(2, '0')}-${currentDate.getDate().toString().padStart(2, '0')}`;

// Set the default value for the date input
document.getElementById("expense-date").value = formattedDate;

// Initialize expenses array from localStorage 
let expenses = 
	JSON.parse(localStorage.getItem("expenses")) || []; 

// Function to render expenses in tabular form 
function renderExpenses() {
    // Clear expense list 
    expenseList.innerHTML = "";

    // Initialize total amount 
    let totalAmount = 0;

    // Loop through expenses array and create table rows 
    for (let i = 0; i < expenses.length; i++) {
        const expense = expenses[i];
        // Format the date as 'd-m-yy'
        const formattedDate = new Date(expense.date).toLocaleDateString('en-GB', {
            day: '2-digit',
            month: '2-digit',
            year: '2-digit'
        });
        const expenseRow = document.createElement("tr");
        expenseRow.innerHTML = `
            <td style="font-size: 18px; height: 30px;">${expense.name}</td>
            <td style="font-size: 18px; height: 30px; text-align:left;">${expense.comment}</td>    
            <td style="font-size: 18px; height: 30px; text-align:right;">${expense.amount.toFixed(2)}</td>
            <td style="font-size: 18px; height: 30px; text-align:center;">${formattedDate}</td>  
            <td>            
                <i class="fas fa-edit edit-icon edit-btn" data-id="${i}"></i>&nbsp&nbsp&nbsp&nbsp
                <i class="fas fa-trash-alt delete-icon delete-btn" data-id="${i}"></i>
            </td>
        `;

        expenseList.appendChild(expenseRow);

        // Update total amount 
        totalAmount += expense.amount;
    }

    // Update total amount display 
    totalAmountElement.textContent = totalAmount.toFixed(2);

    // Check if DataTable is already initialized
    if (!$.fn.DataTable.isDataTable('#expense-table')) {
        expenseTable = $('#expense-table').DataTable({
            lengthMenu: [10, 25, 50, 100, 200], // Set the available "Show entries" options
            pageLength: 10, // Set the default number of records per page
            responsive: true,
            dom: 'lBfrtip',
            buttons: [
                {
                    extend: 'csv',
                    text: 'Export CSV',
                    customize: function(csv) {
                        // Exclude last column (Action) from CSV
                        var rows = csv.split('\n');
                        for (var i = 0; i < rows.length; i++) {
                            var cells = rows[i].split(',');
                            cells.splice(cells.length - 1, 1); // Remove last cell (Action)
                            rows[i] = cells.join(',');
                        }
                        return rows.join('\n');
                    }
                },
                {
                    extend: 'excel',
                    text: 'Export Excel'
                },
                {
                    extend: 'print',
                    text: 'Print',
                    customize: function(win) {					
                        $(win.document.body).find('table').addClass('display').css('font-size', '12px');
                        $(win.document.body).find('thead th:last-child').hide(); // Exclude last th (Action)
                        $(win.document.body).find('tbody td:last-child').hide(); // Exclude last td (Delete)
                    }
                }
            ],
	    order: [[3, 'desc']], // Sort by the fourth column (date) in descending order
		
            initComplete: function() {
                this.api().on('error.dt', function(e, settings, techNote, message) {
                    // Suppress warning messages
                    console.error(message);
                });

                // Add event listener for filtering
                this.api().on('draw.dt', function() {
                    // Recalculate total amount based on visible rows
                    totalAmount = calculateTotalAmount();
                    // Update total amount display 
                    totalAmountElement.textContent = totalAmount.toFixed(2);
                });
            }
        });
    } else {
        // If DataTable is already initialized, recalculate total amount
        totalAmount = calculateTotalAmount();
        // Update total amount display 
        totalAmountElement.textContent = totalAmount.toFixed(2);
    }

    // Save expenses to localStorage 
    localStorage.setItem("expenses", JSON.stringify(expenses));
}

// Function to calculate total amount based on visible rows in the DataTable
function calculateTotalAmount() {
    let totalAmount = 0;
    expenseTable.rows({ search: 'applied' }).every(function() {
        const rowData = this.data();
        totalAmount += parseFloat(rowData[2]); // Assuming the amount is in the third column
    });
    return totalAmount;
}


// Function to add expense 
function addExpense(event) { 
	event.preventDefault(); 

	// Get expense name and amount from form 
	const expenseNameInput = 
		document.getElementById("expense-name"); 
	const expenseAmountInput = 
		document.getElementById("expense-amount"); 
	const expenseName = 
		expenseNameInput.value; 
	const expenseAmount = 
		parseFloat(expenseAmountInput.value);
	const expenseDateInput = 
		document.getElementById("expense-date");
 	const expenseDate =	
		expenseDateInput.value;
		
	const expenseCommentInput = 
		document.getElementById("expense-comment");
 	const expenseComment =	
		expenseCommentInput.value;
			
		
	// Clear form inputs 
	expenseNameInput.value = ""; 
	expenseAmountInput.value = ""; 
	//xpenseDateInput.value = "";
	expenseCommentInput.value = "";
	
	// Validate inputs 
	if (expenseName === "" || isNaN(expenseAmount) || expenseDate === "") { 
		alert("Please enter valid expense details."); 
		return; 
	} 

	// Create new expense object 
	const expense = { 
		name: expenseName,
		comment: expenseComment,	
		amount: expenseAmount,
		date: expenseDate  // Add current date to the expense object		
	}; 
 
	// Add expense to expenses array 
	expenses.push(expense); 
	location.reload();
	// Render expenses 
	renderExpenses(); 
} 

// Function to delete expense
function deleteExpense(event) {
    if (event.target.classList.contains("delete-btn")) {
        // Prompt the user for confirmation before deleting
        if (window.confirm("Are you sure you want to delete this expense?")) {
            // Get expense index from data-id attribute
            const expenseIndex =
                parseInt(event.target.getAttribute("data-id"));

            // Remove expense from expenses array
            expenses.splice(expenseIndex, 1);

            // Render expenses
            renderExpenses();
        }
    }
}

// Add event listeners 
expenseForm.addEventListener("submit", addExpense); 
expenseList.addEventListener("click", deleteExpense); 

// Render initial expenses on page load 
renderExpenses();

// Add event listener for edit button using event delegation
$(document).on('click', '#expense-table .edit-btn', function() {
    // Get the index of the row to edit
    const rowIndex = parseInt($(this).attr('data-id'));

    // Retrieve the expense data for the selected row
    const expense = expenses[rowIndex];

    // Populate form fields with expense data for editing
    document.getElementById("expense-name").value = expense.name;
    document.getElementById("expense-comment").value = expense.comment;
    document.getElementById("expense-amount").value = expense.amount;
    document.getElementById("expense-date").value = expense.date;

    // Remove expense from expenses array
    expenses.splice(rowIndex, 1);

    // Render expenses to update the table
    renderExpenses();
});

// Function to export expense list as CSV
function exportExpenseListAsCSV() {
    // Construct CSV content
    let csvContent = "Expense Name,Amount (Rs),Comment, Date\n";
    expenses.forEach(expense => {
        csvContent += `${expense.name},${expense.amount.toFixed(2)},${expense.comment},${expense.date}\n`;
    });

    // Create a Blob containing the CSV data
    const blob = new Blob([csvContent], { type: 'text/csv' });

    // Create a download link
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = 'expense_list.csv';

    // Trigger the download
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
	console.log(expenses);
}

// Add event listener to export button
$(document).on("click", "#export-button", exportExpenseListAsCSV);

/*
//To initialize and activate DataTable()
$(document).ready(function() {
    $('#expense-table').DataTable({
        paging: true, // Enable pagination
        searching: true, // Enable search box
        ordering: true // Enable column sorting
    });
});

EW488879622IN
*/

// Function to generate printable report
function generateReportPrint() {
    // Retrieve expenses from localStorage
    const expenses = JSON.parse(localStorage.getItem("expenses")) || [];

    // Create a new window for the printable report
    const printWindow = window.open("", "_blank");
	
	// Calculate total amount
    let totalAmount = 0;
    expenses.forEach(expense => {
        totalAmount += expense.amount;
    });

	// Get the current date
    const currentDate = new Date().toLocaleDateString('en-GB', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
    // Write HTML content to the new window
    printWindow.document.write("<html><head><title>Expense Report Print</title>");
    printWindow.document.write('<style>@page { size: landscape; }</style>'); // Set page orientation to landscape
    printWindow.document.write("</head><body>");

    // Add content to the printable report
    printWindow.document.write(`<h2>Expense Report as on ${currentDate}</h2>`);
    printWindow.document.write("<table border='1'><thead><tr><th>Expense Name</th><th>Narration</th><th>Amount (Rs)</th><th>Date</th></tr></thead><tbody>");
    expenses.forEach(expense => {
        const formattedDate = new Date(expense.date).toLocaleDateString('en-GB', {
            day: '2-digit',
            month: '2-digit',
            year: '2-digit'
        });
        printWindow.document.write(`<tr><td>${expense.name}</td><td>${expense.comment}</td><td style="text-align:right;">${expense.amount.toFixed(2)}</td><td>${formattedDate}</td></tr>`);
    });
	 // Print total amount row
    printWindow.document.write(`<tr><td colspan="2" ><strong>Total Amount</strong></td><td style="text-align:right;font-weight:bold;">${totalAmount.toFixed(2)}</td></tr>`);

    printWindow.document.write("</tbody></table>");

    // Close HTML content
    printWindow.document.write("</body></html>");

    // Close the document and display the print dialog
    printWindow.document.close();
    printWindow.print();
}


// Add event listener to the button for generating the report print
document.getElementById("generate-report-btn").addEventListener("click", function() {
    generateReportPrint();
});
