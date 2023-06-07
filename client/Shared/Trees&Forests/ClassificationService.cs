using System.Net.Http.Json;

public class ClassificationService : IClassificationService
{
  private HttpClient _http;

  public ClassificationService(HttpClient http)
  {
    this._http = http;
  }

  public async Task<CorrelationAnalysisResponse> GetCorrelationAnalysis(int fileId, bool containsHeaders)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.CLASSIFICATION}/files/{fileId}/dimensionality"));
    uriBuilder.Query = $"contains_headers={containsHeaders.ToString().ToLower()}";

    return await this._http.GetFromJsonAsync<CorrelationAnalysisResponse>(uriBuilder.Uri.ToString());
  }

  public string GetImageUrl(string resource)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.CLASSIFICATION}/images/{resource}/"));
    string baseAddress = _http.BaseAddress.ToString();
    baseAddress = baseAddress.Substring(0, baseAddress.Length - 1);
    return Path.Join(baseAddress, uriBuilder.Path);
  }

  public async Task<ClassificationSettingsData> GetSettingsData(int fileId)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.CLASSIFICATION}/files/{fileId}/settings"));

    return await this._http.GetFromJsonAsync<ClassificationSettingsData>(uriBuilder.Uri.ToString());
  }

  public async Task SaveSettingsData(ClassificationSettingsData settings)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.CLASSIFICATION}/files/{settings.FileId}/settings"));
    await this._http.PostAsJsonAsync<ClassificationSettingsData>(uriBuilder.Uri.ToString(), settings);
  }

  public async Task<List<object>> GetValidClassVariables(int fileId)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.CLASSIFICATION}/files/{fileId}/valid_class"));

    return await this._http.GetFromJsonAsync<List<object>>(uriBuilder.Uri.ToString());
  }

  public async Task<ClassificationExecutionResponse> GetPrognosisExecutionResponse(int fileId, Dictionary<string, float> register)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.CLASSIFICATION}/files/{fileId}/classify"));
    var message = await this._http.PostAsJsonAsync<Dictionary<string, float>>(uriBuilder.Uri.ToString(), register);
    return await message.Content.ReadFromJsonAsync<ClassificationExecutionResponse>();
  }

  public async Task<ClassificationInfoResponse> GetClassificationInfo(int fileId)
  {
    UriBuilder uriBuilder = new(new Uri(_http.BaseAddress, $"/{(int)AlgorithmType.CLASSIFICATION}/files/{fileId}/info"));

    return await this._http.GetFromJsonAsync<ClassificationInfoResponse>(uriBuilder.Uri.ToString());
  }
}