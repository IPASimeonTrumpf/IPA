function redirect(path) {
    window.location.href = path
}

function send_data() {
    let ip_with_cidr = document.getElementById('ip_with_cidr').value
    if(validate_ip_and_cidr(ip_with_cidr) === true) {
        fetch('/create_network', { method:'POST',
            'headers': {
                'Content-Type': 'Application/json'
            },
            body: JSON.stringify({'ip_with_cidr':ip_with_cidr})
        })
        .then(resp => resp.json())
        .then(data => {
            alert(data['msg'])
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
            return
        }
    console.log('parts')
    console.log(parts)
    } catch {
        error.innerText = 'The IP has an invalid format'
    }
    try {
        parts.forEach(element => {
            let part_as_int = parseInt(element)
            if(part_as_int > 255 || part_as_int < 0) {
                console.log(part_as_int)
                error.innerText = 'The IP has an invalid Value'
                return
            }
        });
    } catch (e) {
        alert(e)
        error.innerText = 'The IP has an invalid Value'
    }
    return true
}