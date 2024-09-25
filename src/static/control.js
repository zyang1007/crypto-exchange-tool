document.getElementById('responseError').style.display = "none";
document.getElementById('responseCurrentConfig').style.display = "none";
document.getElementById('responseInfo').style.display = "none";

// functions control response display
function responseError(){
    document.getElementById('responseError').style.display = "block";
    document.getElementById('responseCurrentConfig').style.display = "none";
    document.getElementById('responseInfo').style.display = "none";
}
function responseCurrentConfig(){
    document.getElementById('responseError').style.display = "none";
    document.getElementById('responseCurrentConfig').style.display = "block";
    document.getElementById('responseInfo').style.display = "none";
}
function responseInfo(){
    document.getElementById('responseError').style.display = "none";
    document.getElementById('responseCurrentConfig').style.display = "none";
    document.getElementById('responseInfo').style.display = "block";
}

// function to get current config 
function getConfig(){
    fetch('/config_grid', {method:'GET'})  // This URL would be the API endpoint
        .then(response => response.json())  // Convert the response to JSON
        .then(data => {
            // Display the fetched data in the paragraph
            document.getElementById('tableConfig1').innerText = data.symbol;
            document.getElementById('tableConfig2').innerText = data.min_price;
            document.getElementById('tableConfig3').innerText = data.max_price;
            document.getElementById('tableConfig4').innerText = data.num_grids;
            document.getElementById('tableConfig5').innerText = data.security_deposit;
            responseCurrentConfig()
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('responseError').innerText = "Config Not Found";
            document.getElementById('responseError').style.color = "#FF0000";
            responseError()
        });
}

// function to handle config form submission
function submitConfig(){
    var isValid = document.querySelector('#configForm').reportValidity();
    if(isValid){
        document.getElementById('responseError').style.display = "none";
        var priceRangeLow = document.getElementById('priceRangeLow').value;
        var priceRangeHigh = document.getElementById('priceRangeHigh').value;
        var numberOfGrids = document.getElementById('numberOfGrids').value;
        var investment = document.getElementById('investment').value;

        //Use Fetch API to send the request
        fetch('/config_grid', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "symbol": "ETH/USDT",
                "min_price": priceRangeLow,
                "max_price": priceRangeHigh,
                "num_grids": numberOfGrids,
                "security_deposit": investment
            }),
        })
        .then(response => response.json())  // Parse the JSON response
        .then(data => {
            // Display the response message in the HTML
            alert(data.message);
            getConfig()
        })
        .catch(error => {
            console.error('Error:', error);
            responseError()
        })
    }
    else{
        document.getElementById('responseError').innerText = "Please input valid config";
        document.getElementById('responseError').style.color = "#FF0000";
        responseError()
    }
}



// Function to fetch data when button is clicked
function getOrderHistory(){
    fetch('/order_history')  // This URL would be the API endpoint
        .then(response => response.json())  // Convert the response to JSON
        .then(data => {
            // Display the fetched data in the paragraph
            document.getElementById('responseInfo').innerHTML = "<b>Order History</b><br>" + JSON.stringify(data);
            responseInfo()
        })
        .catch(error => {
            console.error('Error:', error);
            responseError()
        });
}

// Function to fetch data when button is clicked
function getMarketInfo(){
    fetch('/market_info')  // This URL would be the API endpoint
        .then(response => response.json())  // Convert the response to JSON
        .then(data => {
            // Display the fetched data in the paragraph
            document.getElementById('responseInfo').innerHTML = "<b>Market Info</b><br>" + JSON.stringify(data);
            responseInfo()
        })
        .catch(error => {
            console.error('Error:', error);
            responseError()
        });
}
