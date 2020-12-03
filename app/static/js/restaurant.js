var titleText ={
    props : ['hashtag'],
    template : '<p>{{ title }}</p>',
    data : function(){
        return {
            title : null
        }
    },
    created : function() {
        this.title = this.hashtag.split('#').slice(1,4).join('#');
    }
}
var vm =new Vue({
    el :"#app",
    delimiters:['${', '}'], 
    data :{
        items : [['1','https://scontent-ssn1-1.cdninstagram.com/v/t51.2885-15/sh0.08/e35/s640x640/126305751_1098422653907618_744784791396731771_n.jpg?_nc_ht=scontent-ssn1-1.cdninstagram.com&_nc_cat=102&_nc_ohc=4Anc6Fan7RsAX-kWYyT&tp=1&oh=2c4f4a3ec93ae342713a1f6e3b410703&oe=5FE48CC1', '특제소스인 블랙알리오 소스부터스테이크, 통새우까지 쇽쇽 올라가서 더 맛있는 ㅍㅣ쟈..👏👏👏사이드메뉴랑 같이먹으면 무한흡입각임ㅇㅇ인생피자💖 @@오늘 피자헛 배달시켜먹자( •̀ ω •́ )✧.....', '#블랙알리오스테이크#피자헛#피자헛신메뉴#피자맛집#피자헛블랙알리오스테이크#블랙알리오스테이크피자#피자헛피자추천#피자추천#서울맛집']] 
    },
    components : {
      'title-text' : titleText   
    },
    created : function(){
        var vm =this; 
        axios.post(`${window.origin}/datemaker/restaurant/res`)
        .then((response)=>{
             var resData = response.data;
             vm.items=resData;
        })
        .catch((error)=>{
            console.log(error);
        })
    },
    methods : {
        async addCart(item){
            var item= item.slice(1);
            try {
                await axios.post(`${window.origin}/datemaker/response/cart`, {
                    number: 0,
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

        }});
        
    
 