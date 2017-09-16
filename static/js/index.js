$(() => {
    $('.submitter').on('click', () => {
        let formData = $('#form').serializeArray();
        console.log(formData);
        let sendData = [[], [], [], [], [],]
        formData.forEach((element) => {
            sendData[element.value].push(element.name)
        });
        console.log(sendData);
        $.ajax({
            url: '/result',
            contentType: "application/json",
            type: 'POST',
            data: JSON.stringify({input: sendData}),
            dataType: 'json',
        }).then((data) => {alert(data.result);}, () => {alert('failure');});
    });
});
