var submenuItem = {
    props: ['item'],
    template: '<li v-on:click="passItem">{{ item }}</li>',
    methods: {
        passItem: function () {
            console.log(this.item)
            this.$emit('change', this.item)
        },
    }
}
var vm = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        items: null, 
        selected: '명동',
        selectList: ['광화문','명동','동대문','홍대','여의도','이태원','강남','잠실']
    },
    components: {
        'submenu-item': submenuItem
    },
    created : function(){ 
            this.getData(this.selected); 
    } 
    ,
    methods: {
        changeItem: function (item) {
            this.selected = item
            this.getData(this.selected);  
        },
        getData : function(location){
            var vm = this; 
            axios.post(`${window.origin}/datemaker/seoul/places`,{
                title : location
            })
            .then((response)=>{
                responseData = JSON.parse(JSON.stringify(response.data)); 
                console.log(responseData);
                console.log(typeof responseData);
                vm.items = responseData; 
            })
            .catch((error)=>{
                console.log(error)
            })
        },
        addCart: function (item, index) {
            // var vm = this; 
            // axios.post(`${window.origin}/datemaker/main/slide/food`,{
            //     title : item
            // })
            // .then((response)=>{
            //     responseData = JSON.parse(JSON.stringify(response.data));
            //     vm.items = responseData;
            // })
            // .catch((error)=>{
            //     console.log(error)
            // }
            // )
            console.log(item)
        }
    }
})