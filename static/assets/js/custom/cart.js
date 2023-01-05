function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getToken('csrftoken');



updateBtns=document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        // Assign data atributes to variables
        var productId=this.dataset.product
        var action=this.dataset.action

        // Log data as an object in console
        console.log('productId:',productId, 'action:',action)

        // Request to send the product in the cart
        update_cart(productId,action)
    })
    updateBtns[i].addEventListener('change', function(){
        var productId=this.dataset.product
        var action=this.dataset.action
        if (this.value==='' | this.value==='0'){
            this.nextSibling.getElementsByTagName('input')[0].value=1
        }
        var quantity=this.value

        console.log(productId, action, quantity)
        update_cart(productId, action, quantity)
    })
  }



function update_cart(productId, action, quantity=0){
    var url = 'update-cart' 
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'productId':productId, 'action':action, 'quantity':quantity})
    })
    .then((response)=>response.json())
    .then((data)=>{
        // display new cart items number
        data=JSON.parse(data)
        cartItemsCounters=document.getElementsByClassName('cart-items-count')
        cartTotalCounters=document.getElementsByClassName('cart-total')

        for (var i = 0; i < cartItemsCounters.length; i++){
            cartItemsCounters[i].innerHTML= data.totalCartItems
            console.log(data.message)
        }
        for (var i = 0; i < cartTotalCounters.length; i++){
            cartTotalCounters[i].innerHTML= '$'+parseFloat(data.cartTotal).toFixed(2)
            console.log(data.message)
        }

        productTable=document.getElementsByClassName(productId)[0]
        row=productTable.getElementsByTagName('tr')[0]
        row.getElementsByClassName('orderItem-total')[0].innerHTML= '$'+parseFloat(data.orderItemTotal).toFixed(2)
    })

}





product_form=document.getElementById('product-form')

product_form.addEventListener('submit', function(e){
    e.preventDefault()
    console.log('submitted')
})