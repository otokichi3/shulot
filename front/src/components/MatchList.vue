<template>
	<v-container>
		<v-row class="mt-6 text-center">
			<v-col cols="6" v-for="(match, index) in matchs" :key="match.id">
				<v-card class="light-green lighten-5 mx-auto" cols="12" max-width="400">
					<v-card-title class="subtitle-1 justify-center pt-1 pb-1">
						{{ index + 1 }}コート
					</v-card-title>
					<v-divider></v-divider>
					<v-card-text>
						<v-row>
							<v-col cols="6" :class="{ 'red--text text--accent-1': match.pair1.player1.sex == 2 }"
								class="subtitle-2 pl-1 pr-1">
								{{ match.pair1.player1.name }}
							</v-col>
							<v-col cols="6" :class="{ 'red--text text--accent-1': match.pair1.player2.sex == 2 }"
								class="subtitle-2 pl-1 pr-1">
								{{ match.pair1.player2.name }}
							</v-col>
						</v-row>
						<v-row>
							<v-col col="5" class="mt-3 mb-3 pa-0"><v-divider border-width="100" /></v-col>
							<v-col col="1" class="mr-n3 ml-n3 pa-0">vs</v-col>
							<v-col col="5" class="mt-3 mb-3 pa-0"><v-divider /></v-col>
						</v-row>
						<v-row>
							<v-col cols="6" :class="[match.pair2.player1.sex == 2 ? 'red--text text--accent-1' : '']"
								class="subtitle-2 pl-1 pr-1">
								{{ match.pair2.player1.name }}
							</v-col>
							<v-col cols="6" :class="[match.pair2.player2.sex == 2 ? 'red--text text--accent-1' : '']"
								class="subtitle-2 pl-1 pr-1">
								{{ match.pair2.player2.name }}
							</v-col>
						</v-row>
					</v-card-text>
				</v-card>
			</v-col>
		</v-row>
		<v-row>
			<v-col class="text-center">
				<v-btn color="light-green" min-width="150" :disabled="isMatchFixed || loading" :loading="loading"
					@click="loader = 'loading'; getMatchList();">
					試合を組む
				</v-btn>
			</v-col>
		</v-row>
		<v-row>
			<v-col class="text-center">
				<v-btn color="blue-grey lighten-4" min-width="150" :disabled="isMatchFixed" @click="confirmMatch()">
					試合確定
				</v-btn>
			</v-col>
		</v-row>
		<v-row>
			<v-col class="text-center">
				<v-btn color="blue lighten-4" min-width="150" :disabled="isGameEnd || loading2" :loading="loading2"
					@click="loader = 'loading2'; nextMatch()">
					次の試合
				</v-btn>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios';

export default {
	name: 'MatchList',
	data: () => ({
		isMatchFixed: false,
		isGameEnd: true,
		init_match: [
			{
				pair1: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, },
				pair2: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, }
			},
			{
				pair1: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, },
				pair2: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, }
			},
			{
				pair1: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, },
				pair2: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, }
			},
			{
				pair1: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, },
				pair2: { player1: { name: "　", level: 0, sex: 0, }, player2: { name: "　", level: 0, sex: 0, }, }
			},
		],
		matchs: [],
		create_result: null,
		backend_host: 'http://localhost:8000',
		pair_id: [],
		loader: null,
		loading: false,
		loading2: false,
	}),
	watch: {
		loader() {
			const l = this.loader
			this[l] = !this[l]

			setTimeout(() => (this[l] = false), 1000)

			this.loader = null
		},
	},
	mounted() {
		this.matchs = this.init_match;
	},
	methods: {
		confirmMatch() {
			// 試合確定フラグを立てる
			this.isMatchFixed = true;

			// 確定したペア、組み合わせを登録する
			for (let key in this.matchs) {
				let pair_id = [];
				let pair1 = {
					'player1_id': this.matchs[key].pair1.player1.id,
					'player2_id': this.matchs[key].pair1.player2.id,
				}
				let pair2 = {
					'player1_id': this.matchs[key].pair2.player1.id,
					'player2_id': this.matchs[key].pair2.player2.id,
				}
				Promise.resolve()
					// 組み合わせごとのペアをテーブルに登録する
					.then(() => axios.post(this.backend_host + '/pairs', pair1))
					.then(res => { pair_id.push(res.data) })
					.then(() => axios.post(this.backend_host + '/pairs', pair2))
					.then(res => { pair_id.push(res.data) })
					// 登録したペア二つを組み合わせテーブルに登録する
					.then(() => axios.post(this.backend_host + '/matchs', { 'pair1_id': pair_id[0], 'pair2_id': pair_id[1], },))
					.then(res => { console.log(res) })
					.catch(e => { console.log(e) })
					.finally(() => { pair_id = [] })
			}
			// 次の試合ボタンを活性化する
			this.isGameEnd = false;
		},
		getMatchList() {
			fetch(this.backend_host)
				.then(res => { return res.json() })
				.then(res => {
					setTimeout(() => {
						this.matchs = res.matchs
					}, 700) // TODO: だいたい700msで返って来る、というだけの700
				})
				.catch((error) => console.log(error));
			this.isMatchFixed = false;
		},
		nextMatch() {
			this.isGameEnd = true;
			this.getMatchList();
		},
	}
}
</script>