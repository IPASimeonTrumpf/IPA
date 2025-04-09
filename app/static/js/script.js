function redirect(path) {
    window.location.href = path
}

function send_data() {
    let ip_with_cidr = document.getElementById('ip_with_cidr').value
    ip_with_cidr = validate_ip_and_cidr(ip_with_cidr)
    if(ip_with_cidr != false) {
        spinner = document.getElementById('spinner')
        spinner.style.opacity = 1
        fetch('/create_network', { method:'POST',
            'headers': {
                'Content-Type': 'Application/json'
            },
            body: JSON.stringify({'ip_with_cidr':ip_with_cidr})
        })
        .then(resp => {
            if(!resp.ok) {
                spinner.style.opacity = 0
                let error = document.getElementById('error')
                resp.text().then(data => error.innerText = data)
            } else {
                return resp.json()
            }
        })   
        .then(data => {
            spinner.style.opacity = 0
            alert(data['msg'])
            redirect('/overview')
        })
        .error(resp => resp.json())
        .then(data => {
            alert(data['error'])
        })
    }
}

function validate_ip_and_cidr(ip_with_cidr) {
    let error = document.getElementById('error')
    let cidr = ip_with_cidr.split('/')[1]
    let ip = ip_with_cidr.split('/')[0]
    // validate CIDR
    try {
        cidr_as_int = parseInt(cidr)
    } catch {
        error.innerText = 'The CIDR is not a number'
    }
    if(cidr_as_int > 32 || cidr_as_int < 24) {
        error.innerText = 'The CIDR is not between 23 and 33'
    }

    // validate IP
    let parts = []
    try {
        parts = ip.split('.')
        if(parts.length != 4) {
            error.innerText = 'The IP has an invalid format'
            return false
        }
    } catch {
        error.innerText = 'The IP has an invalid format'
        return false
    }
    try {
        parts.forEach(element => {
            let part_as_int = parseInt(element)
            if(part_as_int > 255 || part_as_int < 0) {
                error.innerText = 'The IP has an invalid Value'
                return false
            }
        });
    } catch (e) {
        error.innerText = 'The IP has an invalid Value'
        return false
    }
    if(!ip_with_cidr.includes('/')) {
        ip_with_cidr += '/32'
    }
    return ip_with_cidr
}