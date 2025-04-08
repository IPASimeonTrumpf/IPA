function scan(host_id, port_list) {
    let option = ''
    if(port_list == 'specific') {
        ports = document.getElementById('specific').value
    } else {
        option = port_list
    }
    fetch('/scan_host', {
        method: 'POST',
        headers: {
            'Content-Type':'Application/json'
        },
        body: JSON.stringify({'host_id': host_id, 'option':option})
    })
    .then(resp => resp.json())
    .then(data => {
        alert(`Scan finished, found ${data.data.length} open ports`)
    })

}