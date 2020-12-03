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
        selected: '잠실/송파/강동',
        selectList: ['잠실/송파/강동', '신사/청담/압구정', '서울역/이태원/용산', '동대문구', '여의도', '구로/신도림/금천', '건대입구/성수/왕십리', '강남/역삼/삼성'
            , '서초/교대/사당', '을지로/명동/중구', '종로/인사동', '홍대/합정/마포/서대문', '영등포역', '김포공항/염창/강서', '성북/강북/노원/도봉']
    },
    components: {
        'submenu-item': submenuItem
    },
    created : function(){ 
            this.getData(this.selected); 
    } 
    ,
    computed: {
        percent: function () {
            let stars = [];
            if(this.items !== null){ 
            Array.prototype.forEach.call(this.items,(item)=>{
                let width = (item[3] / 5) * 100;
                stars.push(width)
            });
        }
            return stars;
        }
    },
    methods: {
        changeItem: function (item) {
            this.selected = item
            this.getData(this.selected);  
        },
        getData : function(location){
            var vm = this; 
            axios.post(`${window.origin}/datemaker/rooms/hotel`,{
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
        async addCart(item) {
            try {
                await axios.post(`${window.origin}/datemaker/response/cart`, {
                    number: 2,
                    item: item,
                    section : 'add'
                })
                alert('상품이 데이트바구니에 담겼습니다.')

            } catch (error) {
                if (error.response.status == 403) { //forbidden
                    alert('로그인 해주세요')
                }
            }
            console.log(JSON.parse(JSON.stringify(item)))
             
        }
    }
})