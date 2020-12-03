var grassBox = {
    props: ['index', 'colors'],
    template: '<div  v-on:click="styleToggle(index,$event);" :style="{backgroundColor : activeColor}" ></div> ',
    data: function () {
        return {
            /*reset data*/
            activeColor: null
        }
    },
    methods: {
        styleToggle: function (index, event) {
            let color = this.colors[index];
            switch (color) {
                case 4:
                    this.colors[index] = 0;
                    event.target.style.backgroundColor = '#EBECEF'
                    break;
                case 3:
                    this.colors[index]++;
                    event.target.style.backgroundColor = '#1E6B36'
                    break;
                case 2:
                    this.colors[index]++;
                    event.target.style.backgroundColor = '#2C9E49'
                    break
                case 1:
                    this.colors[index]++;
                    event.target.style.backgroundColor = '#43c365'
                    break;
                case 0:
                    this.colors[index]++;
                    event.target.style.backgroundColor = '#9CE9AA'
            }
            this.$emit('update')
        },
    },
    created: function () {
        let color = this.colors[this.index];
        switch (color) {
            case 0:  
                this.activeColor = '#EBECEF'
                break;
            case 1:
                this.activeColor = '#9CE9AA'
                break; 
            case 2:
                this.activeColor = '#43c365'
                break;
            case 3:
                this.activeColor = '#2C9E49'
                break
            case 4:
                this.activeColor = '#1E6B36'         
        }
    }
}
var vm = new Vue({
    el: "#app",
    delimiters: ['${', '}'],
    data: {
        /*server data */
        colors: null,
        days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Set', 'Sun'],
        date: null,  //양방향으로 바인딩된 데이터   
        /*reset data */
        profile: false,
        contributions : null,
        names: ['cele1', 'cele2', 'cele3', 'cele4'],
    },
    async created(){
        await this.getData();
        await this.getDate();
        await this.getColors();
    }, 
    components: {
        'grass-box': grassBox
    },
    computed: {
        sendDate: function () {
            if (this.date !== null) {
                return this.date.split('-').join('/');
            } else {
                return null
            }
        },
        
    },
    methods: {
        startProfile: function () {
            if(this.sendDate !== null){
                let day = this.sendDate
                axios.post(`${window.origin}/datemaker/profile/makeprofile`,{
                    day : day
                })
                .then((response)=>{
                    window.location.href = `${window.origin}/datemaker/profile`
                })
                .catch((error)=>{
                    console.log(error);
                })
                }else{
                    alert('날짜를 입력해 주세요')
                }
        },
        getColors : function(){
            var vm = this;
            axios.get(`${window.origin}/datemaker/profile/getcolors`)
            .then(function(response){ 
                vm.colors = response.data['colors']
               
                var arr = vm.colors; 
                console.log(vm.colors);
                console.log(arr);
                vm.getTotal(arr); 
            })
            .catch((error)=>console.log(  error.response.status)); 
        },
        getDate : function(){
            var vm = this;
            axios.get(`${window.origin}/datemaker/profile/getdate`)
            .then(function(response){
                vm.date = Number(response.data['date'])
            })
            .catch((error)=>console.log(error))
        },
        updateDate : function(){
            var colors = this.colors;
            axios.post(`${window.origin}/datemaker/profile/update/date`,{
                colors : colors
            })
            .then(function(response){
                 console.log(response);
            }) 
            .catch((error)=>console.log(error))
        },
        getTotal : function(arr){
            var total =0 ; 
            console.log(arr);
            for(var cnt=0; cnt<arr.length; cnt++){
                total += arr[cnt] 
            }
            this.contributions = total ;
        },
        async renewDate() {
            var vm = this; ;
            try{
                await axios.post(`${window.origin}/datemaker/profile/renew`);
                await vm.getColors();
                console.log("해결됨.");
            }
            catch{
                
            }
        },
        getData : function(){
            var vm = this;
            axios.post(`${window.origin}/datemaker/profile/has`)
            .then(function(response){
                if(response.data['profile'] == 'yes'){
                    vm.profile = true
                }else{
                    console.log('생성안됌');
                }
            })
            .catch((error)=>{ 
                console.log(error.response.status);
                if(error.response.status == 402){
                    alert('세션이 만기되었습니다.')
                    window.location.href = `${window.origin}/`   
                }else{
                    console.log('error',error.response.status);
                }          
            })
            }
    }
});