<svelte:head>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" />

</svelte:head>

<script>
  import { onMount } from 'svelte';
  import { TabulatorFull as Tabulator } from 'tabulator-tables';
  import moment from 'moment';
  import 'tabulator-tables/dist/css/tabulator.min.css';
  import 'tabulator-tables/dist/js/tabulator.min.js';
  import flatpickr from 'flatpickr';
  import 'flatpickr/dist/flatpickr.css';

  let table;
  // let searchData = [];
  // let filteredData = [];

  // let end;
  

  
    onMount(async () => {
      const fetchData = async () => { 
        try {
          const response = await fetch('http://127.0.0.1:5000/api/data');
          const data = await response.json();
          initializeTable(data);

          const start = moment().subtract(365, 'days');
          const end = moment();

          initializeDateRangePicker(start, end);
          fetchFilteredData(start, end);
        } catch (error) {
          console.log(error);
        }
      };

        function handleGlobalSearch(value) {
      table.setFilter(value);
    }

    const initializeTable = (data) => {
      table = new Tabulator('#dataTable', {
        height: '100%',
        layout: 'fitColumns',
        pagination: 'remote',
        paginationSize: 25,
        paginationButtonCount: 5,
        data: data,
        columns: [
          { title: 'First Name', field: 'first_name' },
          { title: 'Last Name', field: 'last_name' },
          { title: 'Company Name', field: 'company_name' },
          { title: 'Address', field: 'address' },
          { title: 'City', field: 'city' },
          { title: 'Country', field: 'county' },
          { title: 'State', field: 'state' },
          { title: 'ZIP', field: 'zip' },
          { title: 'Phone 1', field: 'phone1' },
          { title: 'Phone 2', field: 'phone2' },
          { title: 'Email', field: 'email' },
          { title: 'Web', field: 'web' },
          {
            title: 'Date',
            field: 'date',
            sorter: 'datetime',
            sorterParams: { format: 'DD MMMM YYYY HH:mm:ss' },
          },
        ],
      });
    };

    const fetchFilteredData = (start, end) => {
      if (start && end) {
        fetch(`http://127.0.0.1:5000/api/filtered-data?start_date=${start.format('DD-MM-YYYY HH:mm:ss')}&end_date=${end.format('DD-MM-YYYY HH:mm:ss')}`)
          .then((response) => response.json())
          .then((data) => {
            table.clearData();
            table.setData(data);
          })
          .catch((error) => {
            console.log(error);
          });
      }
    };

    const initializeDateRangePicker = (start, end) => {
      const reportRange = document.getElementById('reportrange');
      const span = reportRange.querySelector('span');

      const formattedStart = start ? start.format('MMMM D, YYYY') : '';
      const formattedEnd = end ? end.format('MMMM D, YYYY') : '';
      const rangeText = `${formattedStart} - ${formattedEnd}`;
      span.textContent = rangeText;

      const flatpickrOptions = {
        mode: 'range',
        dateFormat: 'F j, Y',
        defaultDate: [start.toDate(), end.toDate()],
        onChange: (selectedDates) => {
          const [selectedStart, selectedEnd] = selectedDates.map((date) => moment(date));
          const formattedStart = selectedStart ? selectedStart.format('MMMM D, YYYY') : '';
          const formattedEnd = selectedEnd ? selectedEnd.format('MMMM D, YYYY') : '';
          const rangeText = `${formattedStart} - ${formattedEnd}`;
          span.textContent = rangeText;

          fetchFilteredData(selectedStart, selectedEnd);
        },
      };

      const flatpickrInstance = flatpickr(reportRange, flatpickrOptions);
      flatpickrInstance.setDate([start.toDate(), end.toDate()]);
    };
    


    fetchData();
  });



   // Global search handler
   function handleGlobalSearch(event) {
    const value = event.target.value.trim().toLowerCase();
    if (table) {
      const columnFilterValues = Object.values(columnFilters);
      const globalFilter = function (data) {
        for (const field in data) {
          if (
            columnFilterValues.every(filterValue => data[field].toString().toLowerCase().includes(filterValue)) &&
            (value === '' || Object.values(data).some(val => val.toString().toLowerCase().includes(value)))
          ) {
            return true;
          }
        }
        return false;
      };
      table.setFilter(globalFilter);
    }
  }

    let columnFilters = {};



    function handleColumnSearch(field, value) {
      columnFilters[field] = value.trim().toLowerCase();

      applyFilters();
    }

    function applyFilters() {
      if (table) {
        const combinedFilter = function (data) {
          for (const field in columnFilters) {
            const filterValue = columnFilters[field];
            if (filterValue && !data[field].toString().toLowerCase().includes(filterValue)) {
              return false;
            }
          }
          return true;
        };

        table.setFilter(combinedFilter);
      }
    }


</script>

<style>
  #dataTable {
    height: 100px;
  }

  h1{
    float: center;
  }
  


  
</style>

<h1>Flask MongoDB SVELTE</h1>



<div id="reportrange" style="background: #fff; cursor: pointer; padding: 5px 10px; border: 1px solid #ccc; width: 15%">
  <i class="fa fa-calendar"></i>&nbsp;<span></span> <i class="fa fa-caret-down"></i>
</div>

<br/>

<input type="text" class = "input" style = "width : 7% " placeholder="First Name" on:input="{() => handleColumnSearch('first_name', event.target.value)}">
<input type="text" class = "input"  style = "width : 7% "placeholder="Last Name" on:input="{() => handleColumnSearch('last_name', event.target.value)}">
<input type="text" style = "width : 7% " placeholder="Company name" on:input="{() => handleColumnSearch('company_name', event.target.value)}">
<input type="text"  style = "width : 7% "placeholder="Address" on:input="{() => handleColumnSearch('address', event.target.value)}">
<input type="text" style = "width : 7% " placeholder="City" on:input="{() => handleColumnSearch('city', event.target.value)}">
<input type="text"  style = "width : 6% "placeholder="Country" on:input="{() => handleColumnSearch('county', event.target.value)}">
<input type="text" style = "width : 7% " placeholder="State" on:input="{() => handleColumnSearch('state', event.target.value)}">
<input type="text"  style = "width : 7% "placeholder="Zip" on:input="{() => handleColumnSearch('zip', event.target.value)}">
<input type="text" style = "width : 7% " placeholder="Phone 1" on:input="{() => handleColumnSearch('phone1', event.target.value)}">
<input type="text"  style = "width : 7% "placeholder="Phone 2" on:input="{() => handleColumnSearch('phone2', event.target.value)}">
<input type="text" style = "width : 7% " placeholder="Email" on:input="{() => handleColumnSearch('email', event.target.value)}">
<input type="text"  style = "width : 6% "placeholder="web" on:input="{() => handleColumnSearch('web', event.target.value)}">
<input type="text" style="width: 6%" placeholder="Global Search" class="search" on:input={handleGlobalSearch}>




<div id="dataTable"></div>

