function scan(network_id, port_list) {
    let option = ''
    console.log(port_list)
    console.log(port_list == 'specific')
    if(port_list == 'specific') {
        option = document.getElementById('specific').value
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
        let messages = []
        if(option == 'ping') {
            alert(data.msg)
        } else {
            for(let obj in data.msg) {
                messages.push(JSON.stringify(data.msg))
            }
            alert(messages)
        }
        
        
    })

}