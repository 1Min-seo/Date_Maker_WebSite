var vm = new Vue({
    el : '#app',
    delimiters:['${', '}'],
    data : {
        // server data
        nameList : null,
        total : null,
        today : null, 
        copytoday : null,
        content1 : null,
        content2 : null,
        content3 : null,
        content4 : null, 
        content5 : null,
        content6 : null,
        // reset data 
        topNames : [],
        valueList : [],
        // Chart color
        colorTop : null,
        colorBottom : null,
        //server data
        menu1 : null,
        menu2 : null,
        menu3 : null  
    },
    methods : {
        toInt : function(x){
            return Number(x) 
        }
    },
    created : function(){
        var vm = this
        axios.post(`${window.origin}/datemaker/corona/total`)
        .then(function(response){
            console.log(response);
            const localData = response.data['coronaData'];
            const seoulData = response.data['seoulData'];
            const allData = response.data['allData']; 
            vm.menu1 = allData[2]
            vm.menu2 = allData[0]
            vm.menu3 = allData[1]
            vm.nameList = localData[0];
            vm.total = localData[1] 
            vm.today = localData[2].map((x) =>{return Number(x)});
            vm.copytoday =localData[2].map((x) =>{return Number(x)}); 
            vm.content1 = seoulData[0];
            vm.content2 = seoulData[1];
            vm.content3 = seoulData[2];
            vm.content4 = seoulData[3];
            vm.content5 = seoulData[4]; 
            vm.content6 = seoulData[5];
            vm.getTop5(); 
            vm.setColor();
            vm.makeChart();
        })
        .catch((error)=>{
            console.log(error);
        }) 

    },
    methods : {
        maxCallback : (prev,cur) => {return prev < cur ? cur : prev},
        changeCallback : function(x){
            if(x == this.valueList[this.valueList.length-1]){
                return -1
            }else{
                return x
            }
        },
        getTop5 : function(){
            let cnt = 0;
            while(cnt < 5){
                var max = this.today.reduce(this.maxCallback)
                for(var num of this.copytoday){
                    if(num == max){
                        var maxIndex = this.copytoday.indexOf(num);
                        this.valueList.push(num)
                        this.topNames.push(this.nameList[maxIndex])
                        this.copytoday[maxIndex] = -1
                    } 
                }
                this.today = this.today.map(this.changeCallback); 
                cnt ++ 
            }
        },
        setColor : function(){
                var barColor1 = []
                var barColor2 = [] 
                while(barColor1.length< this.topNames.length){
                    barColor1.push('#4E79A6');
                    barColor1.push('#F18D2B');
                    barColor1.push('#E15659');
                    barColor1.push('#76B7B0');
                }
                while(barColor2.length < this.nameList.length){
                   
                    barColor2.push('#FFC81B');
                    barColor2.push('#5B6777');
                    barColor2.push('#F15B5D');
                    barColor2.push('#1CA392');
                }
                this.colorTop = barColor1.slice(0,this.topNames.length);
                this.colorBottom = barColor2.slice(0,this.nameList.length);    
        },
        makeChart: function(){
            const todayChart = document.getElementById('today-Chart').getContext('2d');
            const localChart = document.getElementById('local-Chart').getContext('2d');
            const seoulChart = document.getElementById('seoul-Chart').getContext('2d'); 
            // 기본 차트 옵션\
            Chart.defaults.global.defaultFontFamily = 'Arials';
            Chart.defaults.global.defaultFontSize = 18;
            Chart.defaults.global.defaultFontColor = "black";

            new Chart(todayChart, {
                type: 'bar', //bar,horizontalBar,pie,line,doughnut,radar, polarArea
                data: {
                    labels:  this.topNames,
                    datasets: [{
                        label: '금일 신규 확진수',
                        data: this.valueList, //인구수 배열
                        //backgroundColor :'green' 모두 한 색으로 바꿀 때
                        backgroundColor: this.colorTop,
                        borderWidth: 2,
                        borderColor: '#ddd',
                        hoverBorderWidth: 2,
                        hoverBorderColor: 'black',
                        lineTension: 0.1
                    }]  
                },
                options: {
                    responsive: true, //반응형인지 아닌지. 
                    title: {
                        display: true,
                        text: '금일 신규발생 확진자 현황 TOP5',
                        fontSize: 20, // 글로벌에 설정한 폰트사이즈를 바꿀 수 있음.
                    },
                    legend: {
                        display:false
                    },
                    tooltips: {
                        enabled: true //마우스 오버시 보이는 숫자
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            })
            new Chart(seoulChart, {
            type: 'doughnut', //bar,horizontalBar,pie,line,doughnut,radar, polarArea
            data: {
                labels: false, //이름 적기
                datasets: [{
                    label: false,
                    data: ['25.4', '74.6'], //인구수 배열
                    //backgroundColor :'green' 모두 한 색으로 바꿀 때
                    backgroundColor: ['dodgerblue','#ddd'],
                    borderWidth: 2,
                    borderColor: '#ddd',
                    hoverBorderWidth: 2,
                    hoverBorderColor: 'black',
                    lineTension: 0.1
                }] //마음에 드는 데이터셋 아무거나 가능
            },
            options: {
                maintainAspectRatio: false,
                responsive: true, 
                title: {
                    display: true,
                    fontSize: 20,  
                },
                legend: {
                    //position : 'right',
                    labels: {
                        fontColor: '#474747',
                        backgroundColor: 'black'
                    }
                },
                tooltips: {
                    enabled: false
                }
            }
            })
            new Chart(localChart, {
                type: 'bar',  
                data: {
                    labels: this.nameList, //이름 적기
                    datasets: [{
                        label: '총 확진수',
                        data:  this.total, //인구수 배열
                        //backgroundColor :'green' 모두 한 색으로 바꿀 때
                        backgroundColor: this.colorBottom,
                        borderWidth: 2,
                        borderColor: '#ddd',
                        hoverBorderWidth: 2,
                        hoverBorderColor: 'black',
                        lineTension: 0.1
                    }] //마음에 드는 데이터셋 아무거나 가능
                },
                options: {
                    responsive: true, //반응형인지 아닌지. 
                    title: {
                        display: true,
                        text: '지역별  확진자 현황',
                        fontSize: 40, // 글로벌에 설정한 폰트사이즈를 바꿀 수 있음.
                    },
                    legend: {
                        display:false
                    },
                    tooltips: {
                        enabled: true //마우스 오버시 보이는 숫자
                    }
                }
            })
        }
    }
});   



 
 