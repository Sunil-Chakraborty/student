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

// Format the date as dd-mm-yyyy
const formattedDate = `${currentDate.getDate().toString().padStart(2, '0')}-${(currentDate.getMonth() + 1).toString().padStart(2, '0')}-${currentDate.getFullYear()}`;

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
	<td class="delete-btn" data-id="${i}">Delete</td> 
	`; 
		expenseList.appendChild(expenseRow); 

		// Update total amount 
		totalAmount += expense.amount; 
	}
	
	
	
	// Initialize DataTable
    $(document).ready(function() {
        $('#expense-table').DataTable();
    });
	
	// Update total amount display 
	totalAmountElement.textContent = 
		totalAmount.toFixed(2); 

	// Save expenses to localStorage 
	localStorage.setItem("expenses", 
		JSON.stringify(expenses)); 
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

	// Render expenses 
	renderExpenses(); 
} 

// Function to delete expense 
function deleteExpense(event) { 
	if (event.target.classList.contains("delete-btn")) { 

		// Get expense index from data-id attribute 
		const expenseIndex = 
			parseInt(event.target.getAttribute("data-id")); 

		// Remove expense from expenses array 
		expenses.splice(expenseIndex, 1); 

		// Render expenses 
		renderExpenses(); 
	} 
} 

// Add event listeners 
expenseForm.addEventListener("submit", addExpense); 
expenseList.addEventListener("click", deleteExpense); 

// Render initial expenses on page load 
renderExpenses();



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

