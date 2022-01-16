//Thêm hàng vào giỏ hàng
function addToCart(id, name, price) {
    event.preventDefault()
    let check_in = document.querySelector('#startdate').value;

    let check_out = document.querySelector('#enddate').value;

    if (check_in > check_out){
        var tmp = check_in;
        check_in = check_out;
        check_out = tmp;
    }
    // promise
    fetch('/api/add-to-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price,
            'check_in': check_in,
            'check_out': check_out
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json()
    }).then(function(data) {
        let d = document.getElementById('cartCounter')
        d.innerText = data.total_quantity
    })
}

//Xác nhận thanh toán
function pay() {
    if (confirm('Ban chac chan thanh toan khong?') == true) {
        fetch('/api/pay', {
            method: 'post'
        }).then(function(res) {
            return res.json()
        }).then(function(data) {
            if (data.code === 200)
                location.reload()
        })
    }
}


//Cập nhật thông tin giỏ hàng
function updateCart(obj, id) {
    fetch('/api/update-cart', {
        method: 'put',
        body: JSON.stringify({
            'id': id,
            'quantity': parseInt(obj.value)
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.code == 200) {
            let d = document.getElementById('cartCounter')
            let d2 = document.getElementById('cartCounter2')
            let amount = document.getElementById('cartAmount')
            d.innerText = data.data.total_quantity
            d2.innerText = data.data.total_quantity
            amount.innerText = data.data.total_amount
        } else if (data.code == 404)
            alert(data.err_msg)
    }).catch(err => console.error(err))
}


//Xóa đơn hàng
function deleteCart(productId) {
    if (confirm('Ban chac chan xoa san pham!!!') == true) {
        fetch(`/api/delete-cart/${productId}`, {
            method: 'delete'
        }).then(res => res.json()).then(data => {
            if (data.code == 200) {
                let d = document.getElementById('cartCounter')
                let d2 = document.getElementById('cartCounter2')
                let amount = document.getElementById('cartAmount')
                d.innerText = data.data.total_quantity
                d2.innerText = data.data.total_quantity
                amount.innerText = data.data.total_amount

                location.reload()
//                let r = document.getElementById(`product${productId}`)
//                r.style.display = 'none'
            } else if (data.code == 404)
                alert(data.err_msg)
        }).catch(err => console.error(err))
    }
}


//Thêm vào comment
function addComment(roomId){
    let content = document.getElementById('commentId')
    if (content !== null){
        fetch('/api/comments',{
            method:'post',
            body:JSON.stringify({
                'room_id' : roomId,
                'content' : content.value
            }),
            headers:{
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data =>{
            if (data.status == 201){
                let c = data.comment

                let area = document.getElementById('commentArea')
                area.innerHTML = `
                    <div class="row">
                        <div class="col-md-1 col-xs-4">
                            <img src="${c.user.avatar}"
                                 class="img-fluid rounded-circle" alt="demo">
                        </div>
                        <div class="col-md-11 col-xs-8">
                            <p>${c.content}</p>
                            <p><em>${moment(c.created_date).fromNow()}</em></p>
                        </div>
                    </div>
                ` + area.innerHTML
            }
            else if(data.status == 404)
                alert(data.err_msg)
        })
    }
}


function addList(){
    var a = document.getElementById('amount').value
    let area = document.getElementById('addListArea')
    area.innerHTML=`<tr>
                        <th>Tên</th>
                        <th>Địa chỉ</th>
                        <th>CMND</th>
                    </tr>`
    let brAdd = document.getElementById('brAddId')
    for(i=0; i<a; i++){
        area.innerHTML = area.innerHTML + `
            <tr>
                <th><input type="text" class="arrival " id="name${i}" name="name${i}"></th>
                <th><input type="text" class="arrival " id="address${i}" name="address${i}"></th>
                <th><input type="text" class="arrival " id="cmnd${i}" name="cmnd${i}"></th>
            </tr>
        `
        brAdd.innerHTML = brAdd.innerHTML + `<br><br><br>`
    }

}