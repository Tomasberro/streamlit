import base64

def get_binary_file_downloader_html(bin_file, file_label='File', file_name='file.csv'):
    with open(file_name, 'wb') as f:
        f.write(bin_file)
    html = '<a href="data:application/octet-stream;base64,{0}" download="{1}">{2}</a>'
    return html.format(bin_file.decode('utf-8').strip(), file_name, file_label)

def get_binary_file_downloader(bin_data, file_label='File'):
    base64_file = base64.b64encode(bin_data).decode()
    href = f'<a href="data:file/csv;base64,{base64_file}" download="{file_label}.csv">CSV File</a>'
    return href
