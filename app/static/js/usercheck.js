var vm = new Vue({
    el : "#app-total",
    delimiters:['${', '}'],
    data : {
        // server data 
        username: null,
        login : false, 
    },
    created : function(){
        this.isLogin()
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
}) 