var trackerInterval = null;
var searchTimeout = null;

$(document).ready(function() {
    updateMarketSummary();
    setInterval(updateMarketSummary, 60000);

    
    $('#tickerInput').on('input', function() {
        var query = $(this).val();
        
        clearTimeout(searchTimeout);
        
        if (query.length < 1) {
            $('#suggestions-box').hide();
            return;
        }

        searchTimeout = setTimeout(function() {
            $.getJSON('/search', { q: query }, function(data) {
                var html = '';
                if (data.length > 0) {
                    data.forEach(function(item) {
                        html += `
                            <div class="suggestion-item" onclick="selectSymbol('${item.symbol}')">
                                <span class="suggestion-symbol">${item.symbol}</span>
                                <span class="suggestion-name">${item.name}</span>
                            </div>
                        `;
                    });
                    $('#suggestions-box').html(html).show();
                } else {
                    $('#suggestions-box').hide();
                }
            });
        }, 300);
    });

    $(document).on('click', function(e) {
        if (!$(e.target).closest('.search-container').length) {
            $('#suggestions-box').hide();
        }
    });
});

function selectSymbol(symbol) {
    $('#tickerInput').val(symbol);
    $('#suggestions-box').hide();
    startTracking(); // 
}



function updateMarketSummary() {
    $.getJSON('/get_market_summary', function(data) {
        var htmlContent = '';
        data.forEach(function(item) {
            var colorClass = item.change >= 0 ? 'positive' : 'negative';
            var arrow = item.change >= 0 ? '▲' : '▼';
            htmlContent += `
                <div class="market-item">
                    <span class="market-name">${item.symbol}</span>
                    <div class="market-price">${item.price.toLocaleString()}</div>
                    <div class="${colorClass}" style="font-size: 0.9rem;">
                        ${arrow} ${Math.abs(item.change)}%
                    </div>
                </div>
            `;
        });
        $('#marketBar').html(htmlContent);
    });
}

function startTracking() {
    var symbol = document.getElementById('tickerInput').value;
    if(!symbol) { alert("Please enter a stock symbol"); return; }
    
    var encodedSymbol = encodeURIComponent(symbol);

    if (trackerInterval) clearInterval(trackerInterval);
    
    $('#displaySymbol').text(symbol.toUpperCase());
    $('#displayPrice').text("...");
    $('#displayChange').text("Loading...");
    $('#displayTime').text("--:--:--");
    $('#displayPrice, #displayChange').removeClass('positive negative');

    updatePrice(encodedSymbol);

    trackerInterval = setInterval(function() {
        updatePrice(encodedSymbol);
    }, 5000);
}

function updatePrice(symbol) {
    $.getJSON('/get_stock_price/' + symbol, function(data) {
        if(data.error) {
            $('#displaySymbol').text("Not Found");
            $('#displayPrice').text("---");
            clearInterval(trackerInterval);
            return;
        }

        $('#displaySymbol').text(data.symbol);
        $('#displayPrice').text(data.price);
        $('#displayChange').text(data.change + '%');
        $('#displayTime').text(data.timestamp);

        $('#displayPrice, #displayChange').removeClass('positive negative');
        if(data.change >= 0) {
            $('#displayPrice, #displayChange').addClass('positive');
        } else {
            $('#displayPrice, #displayChange').addClass('negative');
        }
    }).fail(function() {
        console.log("Network error polling price");
    });
}