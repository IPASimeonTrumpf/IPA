function downloadTextFile(filename, text) {
    // generated by ChatGPT
    const element = document.createElement('a');
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);

    element.setAttribute('href', url);
    element.setAttribute('download', filename);
    element.style.display = 'none';

    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);

    URL.revokeObjectURL(url);
}

function getFormattedDate() {
    // generated by ChatGPT
    const now = new Date();
    const yyyy = now.getFullYear();
    const mm = String(now.getMonth() + 1).padStart(2, '0'); // Monate: 0–11
    const dd = String(now.getDate()).padStart(2, '0');
  
    return `${yyyy}-${mm}-${dd}`;
  }
  
  

function download_results() {
    let host_id = document.getElementById('id').innerText
    let host_ip = document.getElementById('host_ip').innerText
    let filename = "Scan_Result_for_" + host_ip + "_from_" + getFormattedDate() + '.html'
    fetch(`/export_results/${host_id}`)
    .then(resp => resp.text())
    .then(data => {
        downloadTextFile(filename, data)
    })
}