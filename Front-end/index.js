id = 1
var batch_no
var name_of_asset
var manufacturer
var status_of_product
var modalID = exampleModal

function getData() {
    batch_no = document.getElementById('batchNo')
    batch_no = batch_no.value
    name_of_asset = document.getElementById('name')
    name_of_asset = name_of_asset.value
    manufacturer = document.getElementById('manufacturer')
    manufacturer = manufacturer.value
    buyer = document.getElementById('buyer')
    buyer = buyer.value
    quantity = document.getElementById('quantity')
    quantity = quantity.value
    status_of_product = document.getElementById('status')
    status_of_product = status_of_product.value
}


function handleClick() {
    getData()
    if (batch_no !== "" && name_of_asset !== "" && manufacturer != "" && buyer != "" && quantity != "" && status_of_product != "") {
        table_data_reference = document.getElementById('tbody')

        entry = document.createElement('tr')
        entry.setAttribute('id', 'entry')
        ID = document.createElement('td')
        ID.setAttribute('id', 'ID')
        ID.innerText = id
        entry.appendChild(ID)
        table_data_reference.appendChild(entry)

        BATCH_NO = document.createElement('td')
        BATCH_NO.setAttribute('id', 'BATCH_NO')
        BATCH_NO.innerText = batch_no
        entry.appendChild(BATCH_NO)
        table_data_reference.appendChild(entry)

        NAME = document.createElement('td')
        NAME.setAttribute('id', 'NAME')
        NAME.innerText = name_of_asset
        entry.appendChild(NAME)
        table_data_reference.appendChild(entry)

        MANUFACTURER = document.createElement('td')
        MANUFACTURER.setAttribute('id', 'MANUFACTURER')
        MANUFACTURER.innerText = manufacturer
        entry.appendChild(MANUFACTURER)
        table_data_reference.appendChild(entry)

        BUYER = document.createElement('td')
        BUYER.setAttribute('id', 'BUYER')
        BUYER.innerText = buyer
        entry.appendChild(BUYER)
        table_data_reference.appendChild(entry)

        QUANTITY = document.createElement('td')
        QUANTITY.setAttribute('id', 'QUANTITY')
        QUANTITY.innerText = quantity
        entry.appendChild(QUANTITY)
        table_data_reference.appendChild(entry)

        STATUS = document.createElement('td')
        STATUS.setAttribute('id', 'STATUS')
        STATUS.innerText = status_of_product
        entry.appendChild(STATUS)
        table_data_reference.appendChild(entry)
    }
    id = id + 1;
}