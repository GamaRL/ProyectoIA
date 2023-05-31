using System.Net.Http.Json;

public class LogisticRegressionService : ILogisticRegressionService
{
  private HttpClient _http;

  public LogisticRegressionService(HttpClient http)
  {
    this._http = http;
  }

  public async Task<CorrelationAnalysisResponse> GetCorrelationAnalysis(int fileId, bool containsHeaders)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.LOGISTIC_REGRESSION}/files/{fileId}/dimensionality"));
    uriBuilder.Query = $"contains_headers={containsHeaders.ToString().ToLower()}";

    return await this._http.GetFromJsonAsync<CorrelationAnalysisResponse>(uriBuilder.Uri.ToString());
  }

  public string GetImageUrl(string resource)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.LOGISTIC_REGRESSION}/images/{resource}/"));
    string baseAddress = _http.BaseAddress.ToString();
    baseAddress = baseAddress.Substring(0, baseAddress.Length - 1);
    return Path.Join(baseAddress, uriBuilder.Path);
  }

  public async Task<RegressionSettingsData> GetRegressionSettingsData(int fileId)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.LOGISTIC_REGRESSION}/files/{fileId}/settings"));

    return await this._http.GetFromJsonAsync<RegressionSettingsData>(uriBuilder.Uri.ToString());
  }

  public async Task SaveRegressionSettingsData(RegressionSettingsData settings)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.LOGISTIC_REGRESSION}/files/{settings.FileId}/settings"));
    await this._http.PostAsJsonAsync<RegressionSettingsData>(uriBuilder.Uri.ToString(), settings);
  }
}