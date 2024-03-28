// script.js 
// Get form, expense list, and total amount elements 

const expenseForm = 
	document.getElementById("expense-form"); 
const expenseList = 
	document.getElementById("expense-list"); 
const totalAmountElement = 
	document.getElementById("total-amount");
	
const totalRectElement = 
	document.getElementById("total-rect");
const totalPmtElement = 
	document.getElementById("total-exp");
	
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
    // Sort expenses by date in ascending order
    expenses.sort((a, b) => new Date(a.date) - new Date(b.date));

    // Clear expense list 
    expenseList.innerHTML = "";

    // Initialize total amount 
    let totalAmount = 0;
	let totalRect = 0;
	let totalExp = 0;

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
            <td style="font-size: 18px; height: 30px;">${expense.tr}</td>
            <td style="font-size: 18px; height: 30px;text-align:left;">${expense.name}</td>
            <td style="font-size: 18px; height: 30px; text-align:left;">${expense.comment}</td>    
            <td class="${expense.tr === 'Rct' ? 'green-amount' : ''}" style="font-size: 18px; height: 30px; text-align:right;">${expense.amount.toFixed(2)}</td>
            <td style="font-size: 18px; height: 30px; text-align:center;">${formattedDate}</td>  
            <td>            
                <i class="fas fa-edit edit-icon edit-btn" data-id="${i}"></i>&nbsp&nbsp&nbsp&nbsp
                <i class="fas fa-trash-alt delete-icon delete-btn" data-id="${i}"></i>
            </td>
        `;

        expenseList.appendChild(expenseRow);

        // Update total amount based on expense type
        if (expense.tr === 'Rct') {
            totalAmount += expense.amount;
			totalRect += expense.amount;
        } else if (expense.tr === 'Exp') {
            totalAmount -= expense.amount;
			totalExp += expense.amount;
        }
    }

    // Update total amount display 
    totalAmountElement.textContent = totalAmount.toFixed(2);
	totalRectElement.textContent = totalRect.toFixed(2);
	totalPmtElement.textContent = totalExp.toFixed(2);
	
	
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
                }
                
            ],
            order: [[4, 'desc']], // Sort by the fourth column (date) in descending order

            initComplete: function() {
                this.api().on('error.dt', function(e, settings, techNote, message) {
                    // Suppress warning messages
                    console.error(message);
                });

                // Add event listener for filtering
                this.api().on('draw.dt', function() {
                    // Recalculate total amount based on visible rows
					const totals = calculateTotalAmount();
                    //totalAmount = calculateTotalAmount();
                    // Update total amount display 
                    totalAmountElement.textContent = totals.totalAmount.toFixed(2);
					totalRectElement.textContent = totals.totalRect.toFixed(2);
					totalPmtElement.textContent = totals.totalExp.toFixed(2);
				
				});
            }
        });
    } else {
        
        // Update total amount display 
        totalAmountElement.textContent = totalAmount.toFixed(2);
		totalRectElement.textContent = totalRect.toFixed(2);
		totalPmtElement.textContent = totalExp.toFixed(2);
				
	}

    // Save expenses to localStorage 
    localStorage.setItem("expenses", JSON.stringify(expenses));
}
// Define totalRect and totalExp outside the function so they can be accessed globally
let totalRect = 0;
let totalExp = 0;

// Function to calculate total amount based on visible rows in the DataTable
function calculateTotalAmount() {
    let totalRect = 0;
    let totalExp = 0;

    expenseTable.rows({ search: 'applied' }).every(function() {
        const rowData = this.data();
        const expenseType = rowData[0]; // Assuming the expense type is in the first column
        if (expenseType === 'Rct') {
            totalRect += parseFloat(rowData[3]); // Assuming the amount is in the fourth column
        } else if (expenseType === 'Exp') {
            totalExp += parseFloat(rowData[3]); // Assuming the amount is in the fourth column
        }
    });

    // Calculate the total amount based on Rct and Exp separately
    let totalAmount = totalRect - totalExp;
    // Return an object containing all the calculated values
    return {
        totalAmount: totalAmount,
        totalRect: totalRect,
        totalExp: totalExp
    };
}


// Function to add expense 
function addExpense(event) { 
	event.preventDefault(); 

	// Get expense name and amount from form
	const expenseRectInput = 
		document.getElementById("expense-rct");
	const expenseExpInput = 
		document.getElementById("expense-exp");
	
	// Check if either of the radio buttons is checked
	if (!expenseRectInput.checked && !expenseExpInput.checked) {
		alert("Please select an expense type (Rct or Exp).");
		return;
	}

	// Get the selected expense type
	const expenseType = expenseRectInput.checked ? expenseRectInput.value : expenseExpInput.value;
	
	const expenseNameInput = 
		document.getElementById("expense-name");
	const expenseName = 
		expenseNameInput.value;
		
	const expenseAmountInput = 
		document.getElementById("expense-amount");	 
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
	expenseRectInput.checked = false;
	expenseExpInput.checked = false;
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
		tr : expenseType,			
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
	
	if (expense.tr === 'Rct') {
		$("#expense-rct").prop("checked", true);
	} else if (expense.tr === 'Exp') {
		$("#expense-exp").prop("checked", true);
	}
	
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
		if (expense.tr === 'Rct') {
			totalAmount += expense.amount;
		} else if (expense.tr === 'Exp') {
			totalAmount -= expense.amount;
		}
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
    printWindow.document.write(`<h2>Recepts and Payments Report as on ${currentDate}</h2>`);
    printWindow.document.write("<table border='1'><thead><tr><th>Tr.Type</th><th>Expense Name</th><th>Narration</th><th>Amount (Rs)</th><th>Date</th></tr></thead><tbody>");
    expenses.forEach(expense => {
        const formattedDate = new Date(expense.date).toLocaleDateString('en-GB', {
            day: '2-digit',
            month: '2-digit',
            year: '2-digit'
        });
        printWindow.document.write(`<tr><td>${expense.tr}</td><td>${expense.name}</td><td>${expense.comment}</td><td style="text-align:right;">${expense.amount.toFixed(2)}</td><td>${formattedDate}</td></tr>`);
    });
	 // Print total amount row
    printWindow.document.write(`<tr><td colspan="3" ><strong>Net Amount</strong></td><td style="text-align:right;font-weight:bold;">${totalAmount.toFixed(2)}</td></tr>`);

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
