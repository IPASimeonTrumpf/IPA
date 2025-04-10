function scan(host_id, port_list) {
    let option = ''
    if(port_list == 'specific') {
        option = document.getElementById('specific').value
        if(!option.includes(',')) {
            alert('search for atleast 2 ports')
            return
        }
    } else {
        option = port_list
    }
    spinner = document.getElementById('spinner')
    spinner.style.opacity = 1
    fetch('/scan_host', {
        method: 'POST',
        headers: {
            'Content-Type':'Application/json'
        },
        body: JSON.stringify({'host_id': host_id, 'option':option})
    })
    .then(resp => {
        spinner.style.opacity = 0
        if(!resp.ok) {
            resp.text().then(text => alert(text))
        } else {
            return resp.json()
        }
    })
    .then(data => {
        spinner.style.opacity = 0
        
        alert(data.msg)
        
    })

}