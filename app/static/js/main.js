

var vm = new Vue({
    el : "#app",
    delimiters:['${', '}'],
    data :{
      responseData: [],
      foodArray : [],
      number : 0,
      login : false,
      username : null 
    }, 
    created : function(){
            this.isLogin() 
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
    },
    methods : {
        isLogin : function(){
            var vm = this
            axios.get(`${window.origin}/datemaker/main/usercheck`)
            .then((response)=>{ 
                console.log(response); 
                var name = response.data['name']; 
                vm.username = name; 
                vm.login = true; 
            })
            .catch((error)=>{
                console.log(error);
            })
            
        }
    }
}); 

const header = document.getElementsByTagName('header')[0];
document.addEventListener('scroll', () => {
    if (document.documentElement.scrollTop == 0) {
        header.style.boxShadow = '3px 3px 16px #ddd';
    } else {
        header.style.boxShadow = 'none';
    }
});