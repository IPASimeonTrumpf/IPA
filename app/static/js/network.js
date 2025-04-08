function scan(network_id, port_list) {
    let option = ''
    if(port_list == 'specific') {
        ports = document.getElementById('specific').value
    } else {
        option = port_list
    }
    fetch('/scan_network', {
        method: 'POST',
        headers: {
            'Content-Type':'Application/json'
        },
        body: JSON.stringify({'network_id': network_id, 'option':option})
    })
    .then(resp => resp.json())
    .then(data => {
        alert(data.msg)
    })

}