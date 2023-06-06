using System.Net.Http.Json;

public class PrognosisService : IPrognosisService
{
  private HttpClient _http;

  public PrognosisService(HttpClient http)
  {
    this._http = http;
  }

  public async Task<PrognosisSettingsData> GetSettingsData(int fileId)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.PROGNOSIS}/files/{fileId}/settings"));

    return await this._http.GetFromJsonAsync<PrognosisSettingsData>(uriBuilder.Uri.ToString());
  }

  public async Task SaveSettingsData(PrognosisSettingsData settings)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.PROGNOSIS}/files/{settings.FileId}/settings"));
    await this._http.PostAsJsonAsync<PrognosisSettingsData>(uriBuilder.Uri.ToString(), settings);
  }

  public async Task<PrognosisExecutionResponse> GetPrognosisExecutionResponse(int fileId, Dictionary<string, float> register)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.PROGNOSIS}/files/{fileId}/prognosis"));
    var message = await this._http.PostAsJsonAsync<Dictionary<string, float>>(uriBuilder.Uri.ToString(), register);
    return await message.Content.ReadFromJsonAsync<PrognosisExecutionResponse>();
  }

  public async Task<CorrelationAnalysisResponse> GetCorrelationAnalysis(int fileId, bool containsHeaders)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.PROGNOSIS}/files/{fileId}/dimensionality"));
    uriBuilder.Query = $"contains_headers={containsHeaders.ToString().ToLower()}";

    return await this._http.GetFromJsonAsync<CorrelationAnalysisResponse>(uriBuilder.Uri.ToString());
  }

  public string GetImageUrl(string resource)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.PROGNOSIS}/images/{resource}/"));
    string baseAddress = _http.BaseAddress.ToString();
    baseAddress = baseAddress.Substring(0, baseAddress.Length - 1);
    return Path.Join(baseAddress, uriBuilder.Path);
  }
}