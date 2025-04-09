function scan(network_id, port_list) {
    let option = ''
    if(port_list == 'specific') {
        option = document.getElementById('specific').value
    } else {
        option = port_list
    }
    spinner = document.getElementById('spinner')
    spinner.style.opacity = 1
    fetch('/scan_network', {
        method: 'POST',
        headers: {
            'Content-Type':'Application/json'
        },
        body: JSON.stringify({'network_id': network_id, 'option':option})
    })
    .then(resp => {
        if(!resp.ok) {
            resp.text().then(data => alert(data))
        } else {
            return resp.json()
        }
    })
    .then(data => {
        spinner.style.opacity = 0
        let messages = []
        if(option == 'ping') {
            alert(data.msg)
        } else {
            for(let obj in data.msg) {
                messages.push(JSON.stringify(data.msg))
            }
            alert(`found ${messages.length} open ports`)
        }
        
        
    })

}