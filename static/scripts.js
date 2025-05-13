$(document).ready(function() {
    // Initialize DataTable
    var table = $('#usersTable').DataTable({
        pageLength: 5,
        lengthMenu: [5, 10, 20],
        columnDefs: [
            { orderable: false, targets: 3 } // Disable sorting on Actions column
        ]
    });

    

    // Handle row selection (click)
    $('#usersTable tbody').on('click', 'tr', function() {
        $(this).toggleClass('selected');
    });

    // Handle delete action
    $('#usersTable').on('click', '.delete-btn', function(event) {
        event.stopPropagation(); // Prevent triggering row selection
        var row = $(this).closest('tr');
        
        // Confirm deletion
        if (confirm("Are you sure you want to delete this user?")) {
            // Delete the row
            table.row(row).remove().draw();
        }
    });

    // Handle edit action
    $('#usersTable').on('click', '.edit-btn', function(event) {
        event.stopPropagation(); // Prevent triggering row selection
        var rowData = table.row($(this).closest('tr')).data();
        
        // Example: Open an edit form with user data (you can modify this as needed)
        alert('Edit user: ' + rowData[0]); // `rowData[0]` is the Name column
    });
});
