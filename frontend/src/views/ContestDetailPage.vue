<template>
  <div id="contest_detail_page">
    <v-container>
      <div v-if="isLoading" id="skeleton_loaders">
        <v-skeleton-loader type="image" class="my-5"></v-skeleton-loader>
        <v-skeleton-loader type="heading" class="my-2"></v-skeleton-loader>
        <v-skeleton-loader type="list-item-avatar-three-line@3">
        </v-skeleton-loader>
      </div>
      <div v-if="!isLoading">
        <v-img
          v-show="img.show"
          :src="info.imgUrl"
          :max-height="img.height"
          @error="img.show = false"
          @click.stop="(img.showOverlay = true), (img.show = false)"
        >
        </v-img>
        <!-- <v-expand-transition>
          <v-overlay :value="img.showOverlay">
            <div
              @click.stop="(img.showOverlay = false), (img.show = true)"
            >
              <v-img
                :src="info.imgUrl"
                :max-width="img.overlayMaxWidth"
                :max-height="img.overlayMaxHeight"
              >
              </v-img>
            </div>
          </v-overlay>
        </v-expand-transition> -->
        <v-main
          :class="[`text-h3`, `font-weight-medium`]"
          class="transition-swing text--grey"
          v-text="info.title"
        >
        </v-main>
        <v-main
          id="contest_content"
          v-for="i in 10"
          :key="i"
          :class="[`text-h3`, `font-weight-medium`]"
          class="transition-swing text--grey"
          v-text="info.description"
        >
        </v-main>
      </div>
    </v-container>
  </div>
</template>

<script>
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
export default {
  name: "ContestDetailPage",
  inject: ["softReload"],
  mixins: [redirect, snackbar, filter],
  created() {
    this.contestId = this.$route.params.contestId;
    if (!/^\d+$/.test(this.contestId)) {
      this.pageNotFound();
    }
    requestPost({
      url: "/contest/retrieve",
      data: {
        params: this.getContestFilter({
          id: Number(this.contestId),
          detailed: true,
        }),
        pageNum: 0,
        pageSize: 0,
      },
    })
      .then((res) => {
        console.log("no!!!", res);
        this.isLoading = false;
        if (res.data.data.length > 0) {
          this.info = res.data.data[0];

          //TODO: FIXME: remove me later:
          this.info["imgUrl"] =
            "https://timgsa.baidu.com/timg?\
image&quality=80&size=b9999_10000&sec=1606365867398&\
di=747db2a91b640fb0a34a010f4b123299&imgtype=0&src=http%3A%2F%2Fa4.att.hudong.com%\
2F27%2F67%2F01300000921826141299672233506.jpg";

          try {
            this.info["description"] = JSON.parse(this.info["description"]);
          } catch (error) {
            console.log("json parse error", error);
            this.info["description"] = {
              摘要信息: this.info["abstract"],
              注意事项: "竞赛发布者未提供有效的详细描述信息",
            };
          }
          console.log(this.info);
        } else {
          this.pageNotFound();
        }
      })
      .catch((err) => {
        this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
        this.softReload("/search");
        this.isLoading = false;
      });
  },
  data() {
    return {
      contestId: 0,
      isLoading: true,
      info: Object,
      img: {
        show: true,
        showOverlay: false,
        overlayMaxWidth: 1200,
        overlayMaxHeight: 800,
        height: 1200,
      },
    };
  },
  methods: {
    pageNotFound() {
      this.softReload("/pagenotfound");
      this.snackbar("您查找的页面不存在", "error");
    },
    // onScroll(e) {
    //   console.log("haha", this.img.height);
    //   this.img.height = Math.max(0, 400 - e.target.scrollTop);
    // },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
