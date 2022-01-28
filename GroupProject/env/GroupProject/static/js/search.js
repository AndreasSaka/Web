function search() {
    var input, filter, row, products, product, images, box, i, txtValue;
  
    input    = document.getElementById('myInput');
    filter   = input.value.toUpperCase();
    row      = document.getElementById('myRow');
    products = row.getElementsByTagName('h6');
    images   = row.getElementsByTagName('img');
    box      = row.getElementsByClassName('box-element product');
  
    console.log(row);
    console.log(products);
    console.log(images);
    console.log(box);
  
    
    for (i = 0; i < products.length; i++) {
      product = products[i].innerText;
      
      if (product) {
        txtValue = product;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          images[i].style.alignSelf = 'center';
          box[i].style.display = '';
          images[i].style.display = '';
          
        }else {
          box[i].style.display = 'none';
          images[i].style.display = 'none';
        }
      }       
    }	
}