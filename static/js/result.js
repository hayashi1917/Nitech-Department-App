// 色の指定
const LINE_COLOR = "rgba(0,255,0,.8)";
const CHART_COLOR = "rgba(0,255,0,.6)";

let canvas = null;
let ctx = null;

let isLoad = false;

dep_name_dic = {
    "EM": "電気機械工学科",
    "PE": "物理工学科",
    "LC": "応用生命工学科",
    "AC": "社会工学科",
    "CS": "情報工学科",
};

// コンストラクタ
function CustomLegendChartDisplay() {
    this.chart = null;
}
// 読み込み時の処理
$(document).ready(function () {
    // Canvasを取得
    canvas = $("#result_chart");
    ctx = canvas[0].getContext("2d");

    initChart();
    // if(isLoad) {
    // }
    // else {
    //     window.setTimeout(initChart, 1000);
    // }

});
let initChart= () => {
    new CustomLegendChartDisplay().init();
}


CustomLegendChartDisplay.prototype.init = function () {
    const panel = this;
    
    // チャートを表示
    panel.chartDisplay();
}
// 
CustomLegendChartDisplay.prototype.chartDisplay = function () {
    // チャートが存在していれば削除
    if(this.chart != null) {
        this.chart.destroy();
    }
    this.chart = new Chart(ctx, this.getChartProperty());
}

CustomLegendChartDisplay.prototype.getChartProperty = function () {
    let chartProperty = {
      // グラフの種類
    //   type: "horizontalBar",
      type: "bar",
      // データ
      data: this.getChartData(),
      // オプション
      options: this.getChartOptions(),
    };
    return chartProperty;
    /*
    let chartProperty = {
        type: "horizontalBar",
        data: this.getChartData(),
        option: this.getChartOptions(),
    };
    */
};
// 表示するデータの処理
CustomLegendChartDisplay.prototype.getChartData = function () {
    let max = -1;
    let max_n = "";
    let score_dic = {};

    for(let score of score_str.split(',')) {
        let map = score.split(':');
        let scc = Number(map[1]);
        score_dic[map[0]] = scc;

        if(scc > max) {
            max = scc;
            max_n = map[0];
        }
    }

    $("#best_dep").text("あなたに適した学科は: " + dep_name_dic[max_n] + " ");
    $("#comment").text(gpt);

    return {
        labels: [
            dep_name_dic["EM"],
            dep_name_dic["PE"],
            dep_name_dic["LC"],
            dep_name_dic["AC"],
            dep_name_dic["CS"],
        ],
        datasets:[{
            id: "001",
            label: "おすすめ度 ",
            data: [
                score_dic["EM"], 
                score_dic["PE"], 
                score_dic["LC"], 
                score_dic["AC"], 
                score_dic["CS"]
            ]
        },],
    };
}
// 表示するグラフ
CustomLegendChartDisplay.prototype.getChartOptions = function () {
    return {
        plugins: {
            legend: {
                // 凡例の非表示
                display: false,
                maintainAspectRatio: false,
            },
        },
    };
}