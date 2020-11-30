const header = document.getElementsByTagName('header')[0];
document.addEventListener('scroll', () => {
    if (document.documentElement.scrollTop == 0) {
        header.style.boxShadow = '3px 3px 16px #ddd';
    } else {
        header.style.boxShadow = 'none';
    }
});

$('.service-des').slick({
    infinite: true,
    slidesToShow: 1,
    slidesToScroll: 1,
    dots: true,
    autoplay: true
})

var vm = new Vue({
    el : "#app",
    delimiters:['${', '}'],
    data :{
      responseData: [],
      foodArray : [],
      number : 0 
    }, 
    created : function(){
            var vm = this; 
            axios.post(`${window.origin}/datemaker/main/slide/food`)
            .then(function(response){   //성공
                vm.responseData = JSON.parse(JSON.stringify(response.data));
                console.log(JSON.parse(JSON.stringify(response.data)));
                for(; vm.number<30; vm.number+=5 ){
                    var items = vm.responseData.slice(vm.number,vm.number+5); 
                    vm.foodArray.push(items); 
                }; 
                setTimeout(function() { //$(this.$el).find('#carousel')
                    $('.rec-food').slick({
                        infinite: true,
                        slidesToShow: 2,
                        slidesToScroll: 2,
                        autoplay: true
                    });
            },4);}) 
            .catch(function(error){    //실패 
                console.log(error);
            })
    }
}); 

var vm = new Vue({
    el : "#navigation",
    methods : {
        hotelPage : function(){
            window.location.href= `${window.origin}/datemaker/hotel`;
        },
        foodPage : function(){
            window.location.href= `${window.origin}/datemaker/restaurant`;
        },
        PlacePage : function(){
            window.location.href= `${window.origin}/datemaker/dateplace`;
        }
    }

})