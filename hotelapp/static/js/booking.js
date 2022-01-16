var i = 1;
$("#add_row").click(function () {
    console.log("in add row");
  $("#addr" + i).html(
    "<td>" +
      (i + 1) +
      "</td><td><input name='name" +
      i +
      "' type='text' placeholder='Tên' class='form-control input-md'  /></td><td><input  name='country" +
      i +
      "' type='text' placeholder='country'  class='form-control input-md'></td><td><input  name='cmnd" +
      i +
      "' type='text' placeholder='cmnd'  class='form-control input-md'></td><td><input  name='address" +
      i +
      "' type='text' placeholder=''Địa chỉ'  class='form-control input-md'></td>"
  );

  $("#tab_logic").append('<tr id="addr' + (i + 1) + '"></tr>');
  i++;
});
$("#delete_row").click(function () {
  if (i > 1) {
    $("#addr" + (i - 1)).html("");
    i--;
  }
});


function checkIn(){
    console.log("in check in");
};


//Nhân viên tính tiền
function payment(receiptId){
      axios({
        method: 'post',
        url: '/api/booking/payment',
        data:{
          receipt_id: receiptId
        }
      }).then((response)=>{
           data=response.data;
          if (data.code == 200) {
              $('#total_price').val(data.price)
              $('#formPaymentReceipId').val(receiptId)
          } else if (data.code == 404)
              alert(data.err_msg)
    
      }).catch(err => console.error(err))
}



//Nhân viên tính tiền
function paymentSubmit(){
  receiptId =  $('#formPaymentReceipId')
  totalPrice = $('#total_price')
  inPrice = $('#in_price')
  outPrice = $('#out_price')
  if(!receiptId.val() || !totalPrice.val() || !inPrice.val() || !outPrice.val()){
    alert("Vui lòng nhập đầy đủ thông tin")
  }
  else if (totalPrice.val() < 0 || inPrice.val() < 0 || outPrice.val() < 0){
    alert("Giá trị không hợp lệ")

  }
  else if(inPrice.val() < totalPrice.val()){
    alert("Tiền phòng không đủ")
  }
  else{
      axios({
        method: 'post',
        url: '/api/booking/payment',
        data:{
          receipt_id: receiptId.val(),
          total_price: totalPrice.val(),
          in_price: inPrice.val(),

        }
      }).then((response)=>{
          data=response.data;
          if (data.code == 200) {
              alert(data.msg)
              location.reload()


          } else if (data.code == 404)
              alert(data.err_msg)
    
      }).catch(err => console.error(err))
  }


};




//Hủy đặt phòng từ nhân viên
function cancelBooking(receiptId) {
  if (confirm('Hủy đặt phòng') == true) {
      axios({
        method: 'delete',
        url: '/api/booking/cancel-booking',
        data:{
          receipt_id: receiptId
        }
      }).then(res => res.json()).then(data => {
          if (data.code == 200) {
               alert("success")
              location.reload()

          } else if (data.code == 404)
              alert(data.err_msg)
      }).catch(err => console.error(err))
  }
}

