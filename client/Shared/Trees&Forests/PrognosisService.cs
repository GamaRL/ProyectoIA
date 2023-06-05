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
}