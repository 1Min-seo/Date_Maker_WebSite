let piecolorArray; 
let barcolorArray; 
const pieColor = [];
const barColor = []; 
const pieName = [];
const pieNum = [];
const barName =[];
const barNum =[];  
let nameArray,numberArray,addArray;

const req=  new Request(`${window.origin}/corona`,{
    method : "POST",
    credentials : "include",
    cache : "no-cache",
    headers : new Headers({
        "content-type":"application/json;charset=utf-8"
    })
}) 
async function getName(req){
    let response = await fetch(req); //일시 중지 fetch().then((res)=>return res)
    if(response.status !== 200){ //response 객체 
        console.log(`응답 오류 ${response.status}`)
        return ; 
    }
    let res = response.json();
    console.log(res)
    return res   // promise 객체 
} 
getName(req).then((response)=>{
    nameArray = response[0];
    numberArray = response[1];
    addArray =response[2]; 
    setChart()
    makeGraph()
},(error)=>console.log(error)) 

 
function setChart(){  
    pieName =nameArray
    pieNum = addArray
    barName = nameArray
    barNum = numberArray
   
    while(pieColor.length< pieName.length){
        pieColor.push('#EFA8A6');
        pieColor.push('#F6D4CA');
        pieColor.push('#00AEEF');
        pieColor.push('#7C83DB');
    }
    while(barColor.length<25){
        barColor.push('#FFC81B');
        barColor.push('#5B6775');
        barColor.push('#F05B5D');
    } 
    piecolorArray = pieColor.slice(0,pieName.length);
    barcolorArray = barColor.slice(0,25);
// 차트에서캔버스를 사용하려면 context 를 가져와야함   
}

function makeGraph(){ 
    const pieChart = document.getElementById('added').getContext('2d')
    const barChart= document.getElementById('present').getContext('2d');  
    Chart.defaults.global.defaultFontFamily='Arials';
    Chart.defaults.global.defaultFontSize = 18;
    Chart.defaults.global.defaultFontColor = "black"; 

    new Chart(pieChart,{
        type: 'pie', //bar,horizontalBar,pie,line,doughnut,radar, polarArea
        data:{
            labels : pieName, //이름 적기
            datasets: [{
                label:'일별 추가 확진자수',
                data: pieNum,//인구수 배열
                //backgroundColor :'green' 모두 한 색으로 바꿀 때
                backgroundColor : piecolorArray,
                borderWidth : 2,
                borderColor : '#ddd',
                hoverBorderWidth: 2,
                hoverBorderColor: 'black',
                lineTension:0.1
            }] //마음에 드는 데이터셋 아무거나 가능
        },
        options:{
            
            responsive: false,
            title : {
                display : true,
                text : '지역별 일일 추가 확진자 수(추가된 지역)',
                fontSize : 20, // 글로벌에 설정한 폰트사이즈를 바꿀 수 있음.
            },
            legend : {
                
                //position : 'right',
                labels :{
                    fontColor: '#474747',
                    backgroundColor: 'black' 
                }
            },
            layout: {
                padding : {
                    left : 60,
                    right: 0,
                    bottom : 0,
                    top : 60
                }
            },
            tooltips : {
                enabled : true //마우스 오버시 보이는 숫자
            }
        }
    })         
    
    new Chart(barChart,{
        type: 'bar', //bar,horizontalBar,pie,line,doughnut,radar, polarArea
        data:{
            labels : barName, //이름 적기
            datasets: [{
                label:'확진자 수',
                data: barNum,//인구수 배열
                //backgroundColor :'green' 모두 한 색으로 바꿀 때
                backgroundColor : barcolorArray,
                borderWidth : 2,
                borderColor : '#ddd',
                hoverBorderWidth: 2,
                hoverBorderColor: 'black',
                lineTension:0.1
            }] //마음에 드는 데이터셋 아무거나 가능
        },
        options:{
            responsive: false,
            title : {
                display : true,
                text : '지역별 확진자 수',
                fontSize : 23, // 글로벌에 설정한 폰트사이즈를 바꿀 수 있음.
            },
            legend : {
                display:false,
                //position : 'right',
                labels :{
                    fontColor: 'blue',
                    backgroundColor: 'black' 
                }
            },
            layout: {
                padding : {
                    left : 0,
                    right: 0,
                    bottom : 0,
                    top : 50
                }
            },
            tooltips : {
                enabled : true //마우스 오버시 보이는 숫자
            },
            scales : {
                yAxes : [{
                    ticks : { 
                        min : 0 , //0 부터 시작
                        stepSize : 45//y축 간격
                    }
                }],
                xAxes:[{
                    ticks:{
                        fontSize : 8
                    },
                    gridLines:{
                        lineWidth: 0
                    }
                }]
            }
        }
    })
}
