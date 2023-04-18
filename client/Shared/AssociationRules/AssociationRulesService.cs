using System.Net.Http.Json;
using System.Text.Json;
using System.Net.Http.Headers;
using System.Web;

public class AssociationRulesService : IAssociationRulesService
{
  private HttpClient _http;

  public AssociationRulesService(HttpClient http)
  {
    this._http = http;
  }

  public async Task<List<AssociationRulesResponse>> GetAssociationRules(int fileId, float min_support, float min_confidence, float min_lift)
  {
    string url = GetAssociationRulesUrl(fileId, min_support, min_confidence, min_lift);
    return await this._http.GetFromJsonAsync<List<AssociationRulesResponse>>(url);
  }

  public string GetAssociationRulesUrl(int fileId, float minSupport, float minConfidence, float minLift)
  {
    UriBuilder uriBuider = new(new Uri(_http.BaseAddress, $"/1/rules/{fileId}"));
    string queryString = $"min_support={minSupport:0.00}&min_confidence={minConfidence:0.00}&min_lift={minLift:0.00}";
    queryString = queryString.Replace(",", ".");
    uriBuider.Query = queryString;
    return uriBuider.Uri.ToString();
  }

  public async Task<List<AssociationRulesExecResponse>> GetExecRules(int fileId)
  {
    return await this._http.GetFromJsonAsync<List<AssociationRulesExecResponse>>($"1/rules/{fileId}/all");
  }

  public async Task<FileContentModel> GetFileContent(int fileId)
  {
    var response = await this._http.GetAsync($"1/files/{fileId}");
    return  await response.Content.ReadFromJsonAsync<FileContentModel>();
  }

  public async Task<List<FileModel>> GetFiles()
  {
    var response = await this._http.GetAsync("1/files");
    return await response.Content.ReadFromJsonAsync<List<FileModel>>();
  }

  public string GetFileUrl(int fileId)
  {
    UriBuilder uriBuider = new(new Uri(_http.BaseAddress, $"/1/files/{fileId}"));
    uriBuider.Query = "download=true";
    return uriBuider.Uri.ToString();
  }

  public async Task<List<FrequencyAnalysisResponse>> GetFrequencies(int fileId)
  {
    return await this._http.GetFromJsonAsync<List<FrequencyAnalysisResponse>>($"1/statistics/{fileId}");
  }

  public async Task<FileModel> RemoveFile(int id)
  {
    var response = await this._http.DeleteAsync($"1/files/{id}");
    return await response.Content.ReadFromJsonAsync<FileModel>();
  }

  public async void SaveRules(int fileId, List<AssociationRulesResponse> rules)
  {
    string data = JsonSerializer.Serialize(rules);
    Console.WriteLine(data);
    var content = new StringContent(data, new MediaTypeHeaderValue("application/json"));
    var response = await this._http.PostAsync($"1/rules/{fileId}", content);
  }
}